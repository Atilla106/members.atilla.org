'''Model definition for the ethernet authentication application.'''
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

# Constants used to describe a SwitchPort status
AUTO = 'AUTO'
AUTHORIZED = 'AUTHORIZED'
UNAUTHORIZED = 'UNAUTHORIZED'
SWITCH_PORT_STATE = (
    (AUTO, 'Automatique'),
    (AUTHORIZED, 'Ouvert'),
    (UNAUTHORIZED, 'Fermé')
)


class Switch(models.Model):
    '''
    Define a switch that contains ports configured to work with 802.1x authentication.

    Some settings of the switch, such as the username that should be used for telnet connection,
    the password and the telnet adaptater should be defined in the platform configuration.
    '''

    name = models.CharField('Name', max_length=32, unique=True)
    description = models.CharField('Description', max_length=255, blank=True)

    ip_address = models.GenericIPAddressField('IP address', protocol='IPv4', unique=True)

    def __str__(self):
        return '{} - {} ({})'.format(self.name, self.description, self.ip_address)


class SwitchPort(models.Model):
    '''Define a switch port.'''

    switch = models.ForeignKey(Switch, on_delete=models.CASCADE)

    label = models.CharField('Label', max_length=32)
    name = models.CharField('Name', max_length=16)

    default_state = models.CharField('Default state', max_length=12, choices=SWITCH_PORT_STATE, default=AUTO)

    # Though we can get the current state of the switch port using the SwitchPortAction model,
    # this field allows to store the _actual_ value of the switch port (and not the value that can be
    # extrapolated from the SwitchPortAction model).
    #
    # This is useful especially in cases where the switch update fails.
    current_state = models.CharField('Current state', max_length=12, choices=SWITCH_PORT_STATE, default=AUTO)

    last_modified = models.DateTimeField('Last update', auto_now=True)

    def __str__(self):
        return '{} - {} ({})'.format(self.label, self.name, self.switch.name)


class SwitchPortAction(models.Model):
    '''
    Define an action made on a given switch port.

    This model is also responsible for defining expiracy timestamps for actions made on switch ports.
    Note that for each port, only one action should be active at the time.
    '''

    switch_port = models.ForeignKey(SwitchPort, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    new_state = models.CharField('New state', max_length=12, choices=SWITCH_PORT_STATE)

    add_date = models.DateTimeField('Date added', auto_now_add=True)
    expiration_date = models.DateTimeField('Expiration date')

    def save(self, *args, **kwargs):
        concurrent_action = SwitchPortAction.objects.filter(switch_port=self.switch_port,
                                                            expiration_date__gt=timezone.now()).first()
        if concurrent_action is not None and concurrent_action != self:
            raise ValidationError('Another action is currently active on this port')

        return super(SwitchPortAction, self).save(*args, **kwargs)

    def __str__(self):
        return '{} - {} ({})'.format(self.switch_port.label, self.user, self.expiration_date)

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.db import models


def get_new_IP_address():
    '''Generates a new IP address for the device.'''
    def lastMember(device):
        return int(device.device_ip.split('.')[3])

    used_members = list(map(lastMember, Device.objects.all()))
    available_IPs = ([
        a for a in range(settings.IP_RANGE_START, settings.IP_RANGE_END)
        if a not in used_members
    ])

    if len(available_IPs) == 0:
        raise ValidationError('No more available IPs!')

    return settings.IP_NETWORK_PREFIX + str(available_IPs[0])


class Device(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Only accept a device name composed of alphanumeric characters, - and _
    device_name = models.CharField(
        max_length=25,
        validators=[
            RegexValidator(
                regex='^[-a-zA-Z0-9]{1,25}$',
                message='Invalid name',
            )
        ],
    )

    device_ip = models.GenericIPAddressField(
        protocol='IPv4',
        unique=True,
    )

    description = models.CharField(
        max_length=255,
        blank=True,
    )

    add_date = models.DateTimeField(
        'Date added',
        auto_now_add=True,
    )

    last_modified = models.DateTimeField(
        'Last update',
        auto_now=True,
    )

    def clean(self):
        '''Check if the user has not another device with the same name, then
        assign a new IP address if needed.'''
        if (
            self.user_id is not None and
            self.device_name in [
                d.device_name for d in self.user.device_set.all()
                if d.id != self.id
            ]
        ):
            raise ValidationError('Device name aleready taken')

        if self.device_ip is None:
            self.device_ip = get_new_IP_address()

        return super(Device, self).clean()

    def save(self, *args, **kwargs):
        device_count = self.user.device_set.all().count()
        if device_count >= settings.MAX_DEVICE_PER_USER:
            raise ValidationError('Too many devices')

        return super(Device, self).save(*args, **kwargs)

    def __str__(self):
        return '{name} ({description})'.format(
            name=self.device_name,
            description=self.description,
        )

    def get_absolute_url(self):
        return reverse('network:device_detail', kwargs={'pk': self.pk})

    def get_FQDN(self):
        return '{name}.{username}.{domain}'.format(
            name=self.device_name,
            username=self.user.username,
            domain=settings.DNS_DOMAIN,
        )

    def get_last_ip_block(self):
        return int(self.device_ip.split('.')[3])

    class Meta:
        permissions = (
            ('can_publish_device', 'Can use this device on the network'),
        )

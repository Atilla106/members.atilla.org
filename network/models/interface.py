from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.db import models

from .device import Device


# Constants for interface type
WIFI = 'WLP'
ETHERNET = 'ETH'
INTERFACE_TYPE_CHOICES = (
    (WIFI, 'Wifi'),
    (ETHERNET, 'Ethernet'),
)


class Interface(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)

    interface_type = models.CharField(
        max_length=3,
        choices=INTERFACE_TYPE_CHOICES,
        default=ETHERNET,
    )

    mac_address = models.CharField(
        max_length=17,
        validators=[
            RegexValidator(
                regex='^([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})$',
                message='Invalid MAC address',
            )
        ],
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

    def save(self, *args, **kwargs):
        interface_count = self.device.interface_set.all().count()
        if interface_count >= settings.MAX_INTERFACE_PER_DEVICE:
            raise ValidationError('Too many interfaces')
        return super(Interface, self).save(*args, **kwargs)

    def __str__(self):
        return '{mac} - {interface_type} (description{})'.format(
            mac=self.mac_address,
            interface_type=self.interface_type,
            description=self.description,
        )

    def get_absolute_url(self):
        return reverse('network:device_detail', kwargs={'pk': self.device.pk})

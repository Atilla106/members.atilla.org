import re

from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from .settings import IP_NETWORK_PREFIX, IP_RANGE_START, IP_RANGE_END
from .settings import DNS_DOMAIN

""" Generates a new IP address for the device """
def getNewIPAddress():
    def lastMember(device):
        return int(device.device_ip.split(".")[3])

    usedMembers = list(map(lastMember, Device.objects.all()))
    availableIPs = ([a for a in range(IP_RANGE_START, IP_RANGE_END)
        if a not in usedMembers])

    if len(availableIPs) == 0:
        raise ValidationError("No more available IPs !")
    return IP_NETWORK_PREFIX + str(availableIPs[0])

""" Models definition """

class Device(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    """ Only accept a device name composed of alphanumeric characters
    and - and _ """
    device_name = models.CharField(
            max_length=25,
            validators=[RegexValidator(
                regex="^[a-zA-Z0-9_−]{1,25}$",
                message="Invalid name")])

    device_ip = models.GenericIPAddressField(
            protocol="IPv4",
            unique=True)

    description = models.CharField(
            max_length=255,
            blank=True)

    add_date = models.DateTimeField(
            "Date added",
            auto_now_add=True)

    last_modified = models.DateTimeField(
            "Last update",
            auto_now=True)

    """ Check if the user has not another device with the same name, then assign
    a new IP address if needed """
    def clean(self):
        if ((self.user_id is not None)
            and (self.device_name
                in [d.device_name for d in self.user.device_set.all()
                    if d.id != self.id])):
                raise ValidationError('Device name aleready taken')
        if (self.device_ip is None):
            self.device_ip = getNewIPAddress()

    def __str__(self):
        return self.device_name + " (" + self.description + ")"

    def get_absolute_url(self):
        return reverse('network:deviceDetail', kwargs={'pk': self.pk})

    def getFQDN(self):
        return self.device_name + "." + self.user.username + "." + DNS_DOMAIN

class Interface(models.Model):
    WIFI = "WLP"
    ETHERNET = "ETH"
    INTERFACE_TYPE_CHOICES = (
            (WIFI, "Wifi"),
            (ETHERNET, "Ethernet")
            )

    device = models.ForeignKey(Device, on_delete=models.CASCADE)

    interface_type = models.CharField(
            max_length=3,
            choices=INTERFACE_TYPE_CHOICES,
            default=ETHERNET)

    mac_address = models.CharField(
            max_length=17,
            validators=[RegexValidator(
                regex="^([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})$",
                message="Invalid MAC address")],
            unique=True)

    description = models.CharField(
            max_length=255,
            blank=True)

    add_date = models.DateTimeField(
            "Date added",
            auto_now_add=True)

    last_modified = models.DateTimeField(
            "Last update",
            auto_now=True)

    def __str__(self):
        return (self.mac_address + " - " + self.interface_type
        + " (" + self.description + ")")

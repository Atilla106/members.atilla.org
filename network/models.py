import re

from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from .settings import IP_NETWORK_PREFIX, IP_RANGE_START, IP_RANGE_END

""" Custom validator to prevent a user to add another device with the same name
as a previous one """
"""def validate_device_name(value):"""

""" Models definition """

class Device(models.Model):

    """ Generates a new IP address for the device """
    def IPAddress():
        def lastMember(device):
            return int(device.device_ip.split(".")[3])
        usedMembers = list(map(lastMember, Device.objects.all()))
        return IP_NETWORK_PREFIX + str(0)

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
            unique=True,
            default=IPAddress)

    description = models.CharField(
            max_length=255,
            blank=True)

    add_date = models.DateTimeField(
            "Date added",
            auto_now_add=True)

    last_modified = models.DateTimeField(
            "Last update",
            auto_now=True)

    def clean(self):
        if (self.device_name
            in [d.device_name for d in self.user.device_set.all()]):
                raise ValidationError('Device name aleready taken')

    def __str__(self):
        return self.device_name + " (" + self.description + ")"

    def GetFQDN(self):
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

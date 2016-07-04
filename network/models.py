import re

from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator

from django.contrib.auth.models import User

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

    def __str__(self):
        return self.device_name + " (" + self.description + ")"

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

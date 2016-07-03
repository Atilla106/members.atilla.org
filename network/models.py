from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device_name = models.CharField(
            max_length=25
            validator=[validate_device_name])
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
            auto_now=True,
            auto_now_add=True)

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
            max_length=17
            validator=[validate_mac_format]
            unique=True)
    description = models.CharField(
            max_length=255,
            blank=True)
    add_date = models.DateTimeField(
            "Date added",
            auto_now_add=True)
    last_modified = models.DateTimeField(
            "Last update",
            auto_now=True,
            auto_now_add=True)

    def __str__(self):
        return (self.mac_address + " - " + self.interface_type
        + " (" + self.description + ")")

from django.contrib import admin

from .models.device import Device
from .models.interface import Interface

admin.site.register(Device)
admin.site.register(Interface)

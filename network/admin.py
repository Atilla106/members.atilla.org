from django.contrib import admin

from .models.device import Device
from .models.interface import Interface
from members.settings import MAX_INTERFACE_PER_DEVICE


class InterfaceAdmin(admin.TabularInline):
    model = Interface
    max_num = MAX_INTERFACE_PER_DEVICE
    display = ('interface', 'mac_address', 'description')
    view_on_site = False


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('user', 'device_name', 'description', 'add_date')
    readonly_fields = ('device_ip',)
    search_fields = ['user__username']
    inlines = [InterfaceAdmin]

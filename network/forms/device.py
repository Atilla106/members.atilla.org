from django.forms import ModelForm
from django.forms import TextInput
from ..models.device import Device


class DeviceForm(ModelForm):
    class Meta:
        model = Device
        fields = ['device_name', 'description']
        widgets = {
            'device_name': TextInput(attrs={
                'pattern': '[-a-zA-Z0-9]{1,25}$',
                'placeholder': 'Caractères alphanumériques et "-"',
            }),
        }

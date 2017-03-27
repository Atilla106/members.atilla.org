from django import forms

from ..models.interface import (
    Interface,
    INTERFACE_TYPE_CHOICES,
)


class InterfaceForm(forms.ModelForm):
    '''Form declaration for the interface model.'''
    interface_type = forms.ChoiceField(choices=INTERFACE_TYPE_CHOICES)

    class Meta:
        model = Interface
        fields = ['interface_type', 'mac_address', 'description']
        widgets = {
                'mac_address': forms.TextInput(
                    attrs={
                        'pattern': '^([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})$',
                        'placeholder': '12:56:90:ab:cd:ef'
                    }
                ),
        }

from django.forms import ModelForm

from .models import SwitchPortAction


class SwitchPortActionForm(ModelForm):
    class Meta:
        model = SwitchPortAction
        fields = ['new_state', 'expiration_date']

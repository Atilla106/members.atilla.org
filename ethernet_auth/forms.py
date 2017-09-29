from django.forms import ModelForm
from django.forms import SplitDateTimeWidget

from .models import SwitchPortAction


class SwitchPortActionForm(ModelForm):
    class Meta:
        model = SwitchPortAction
        fields = ['new_state', 'expiration_date']
        widgets = {
            'expiration_date': SplitDateTimeWidget()
        }

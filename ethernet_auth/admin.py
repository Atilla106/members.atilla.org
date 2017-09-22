from django.contrib import admin

from .models import Switch
from .models import SwitchPort
from .models import SwitchPortAction


admin.site.register(Switch)
admin.site.register(SwitchPort)
admin.site.register(SwitchPortAction)

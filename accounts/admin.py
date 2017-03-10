from django.contrib import admin

from .models import PendingUser
from .models import Account


admin.site.register(PendingUser)
admin.site.register(Account)

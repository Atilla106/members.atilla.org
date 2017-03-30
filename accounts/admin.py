from django.contrib import admin

from .models import PendingUser
from .models import Account


class AccountAdmin(admin.ModelAdmin):
    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

    def get_username(self, obj):
        return obj.user.username

    get_first_name.admin_order_field = 'user__first_name'
    get_first_name.short_description = 'First name'

    get_last_name.admin_order_field = 'user__last_name'
    get_last_name.short_description = 'Last Name'

    get_username.admin_order_field = 'user__username'
    get_username.short_description = 'Username'

    list_display = ('get_first_name', 'get_last_name', 'get_username')


admin.site.register(PendingUser)
admin.site.register(Account, AccountAdmin)

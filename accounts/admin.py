from django.contrib import admin

from .models import PendingUser
from .models import Account


def mark_paid_membership(model, request, querySet):
    accounts = querySet.all()

    for account in accounts:
        account.has_paid_membership = True
        account.save(update_fields=['has_paid_membership'])


def remove_paid_membership(model, request, querySet):
    accounts = querySet.all()

    for account in accounts:
        account.has_paid_membership = False
        account.save(update_fields=['has_paid_membership'])


class AccountAdmin(admin.ModelAdmin):
    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

    def get_username(self, obj):
        return obj.user.username

    def has_paid_membership(self, obj):
        return obj.has_paid_membership

    # Add a custom action in order to add / remove the membership flag to the accounts
    actions = [mark_paid_membership, remove_paid_membership]

    get_first_name.admin_order_field = 'user__first_name'
    get_first_name.short_description = 'First name'

    get_last_name.admin_order_field = 'user__last_name'
    get_last_name.short_description = 'Last Name'

    get_username.admin_order_field = 'user__username'
    get_username.short_description = 'Username'

    has_paid_membership.admin_order_field = 'account__has_paid_membership'
    has_paid_membership.short_description = 'Has paid the membership fee?'

    list_display = ('get_first_name', 'get_last_name', 'get_username', 'has_paid_membership')


admin.site.register(PendingUser)
admin.site.register(Account, AccountAdmin)

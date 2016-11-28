from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Permission


def make_publisher(modeladmin, request, queryset):
    users = queryset.all()
    perm = Permission.objects.get(codename='can_publish_device')

    for user in users:
        user.user_permissions.add(perm)


make_publisher.short_description = "Add publish device permission"


def remove_publisher(modeladmin, request, queryset):
    users = queryset.all()
    perm = Permission.objects.get(codename='can_publish_device')

    for user in users:
        user.user_permissions.remove(perm)


remove_publisher.short_description = "Remove publish device permission"


class CustomUserAdmin(UserAdmin):
    actions = [make_publisher, remove_publisher]


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

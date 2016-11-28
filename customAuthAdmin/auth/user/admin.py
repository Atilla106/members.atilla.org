from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Permission


def make_publisher(modeladmin, request, queryset):
    users = queryset.all()
    perm = Permission.objects.get(codename='can_publish_device')

    for user in users:
        user.user_permissions.add(perm)


make_publisher.short_description = 'Ajouter les droits de publication'


def remove_publisher(modeladmin, request, queryset):
    users = queryset.all()
    perm = Permission.objects.get(codename='can_publish_device')

    for user in users:
        user.user_permissions.remove(perm)


remove_publisher.short_description = 'Supprimer les droits de publication'


class CustomUserAdmin(UserAdmin):
    def is_allowed_publish_device(self, obj):
        return obj.has_perm('network.can_publish_device')

    is_allowed_publish_device.short_description = 'Peut publier'

    actions = [make_publisher, remove_publisher]

    list_display = [
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_allowed_publish_device']

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

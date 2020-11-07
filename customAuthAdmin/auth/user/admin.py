from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Permission
from django.db.models import Q

from customAuthAdmin.auth.forms import CustomUserChangeForm


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


class CanPublishListFilter(admin.SimpleListFilter):
    title = ('droit de publication')
    parameter_name = 'publisher'

    def lookups(self, request, modeladmin):
        return(
            ('True', 'Oui'),
            ('False', 'Non')
        )

    def queryset(self, request, queryset):
        perm = Permission.objects.get(codename='can_publish_device')

        if self.value() == 'True':
            qs = queryset.filter(Q(user_permissions=perm) | Q(is_staff='True'))
        elif self.value() == 'False':
            qs = queryset.exclude(
                Q(user_permissions=perm) |
                Q(is_staff='True')
            )
        else:
            qs = queryset.all()
        return qs


class CustomUserAdmin(UserAdmin):
    def is_allowed_publish_device(self, obj):
        return obj.has_perm('network.can_publish_device')

    is_allowed_publish_device.short_description = 'Peut publier'
    is_allowed_publish_device.boolean = True

    actions = [make_publisher, remove_publisher]

    form = CustomUserChangeForm

    list_display = [
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_allowed_publish_device']

    list_filter = UserAdmin.list_filter + (CanPublishListFilter,)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

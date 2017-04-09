from django.contrib.auth.models import Permission, User
from django.db.models.signals import post_save
from django.dispatch import receiver

from constance import config
from .models import Account


@receiver(post_save, sender=User)
def auto_add_publish_perm(sender, instance, created, **kwargs):
    if config.AUTO_ALLOW_FLAG and created:
        perm = Permission.objects.get(codename='can_publish_device')

        instance.user_permissions.add(perm)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)

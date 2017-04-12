from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Permission

from constance import config


@receiver(post_save, sender=User)
def auto_add_publish_perm(sender, instance, created, **kwargs):
    if config.AUTO_ALLOW_FLAG and created:
        perm = Permission.objects.get(codename='can_publish_device')

        instance.user_permissions.add(perm)

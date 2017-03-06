'''Account models definition.'''
import base64
import hashlib
import hmac
import time

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save


class PendingUser(models.Model):
    username = models.CharField(max_length=10, unique=True)

    first_name = models.CharField('First name', max_length=25)

    last_name = models.CharField('Last name', max_length=25)

    email = models.EmailField('E-Mail', max_length=50, unique=True)

    validation_token = models.CharField('Validation token', max_length=256)

    add_date = models.DateTimeField('Date added', auto_now_add=True)

    last_modified = models.DateTimeField('Last update', auto_now=True)

    def generate_username(self):
        '''Generates a proper username.

        TODO: check if the username is not aleready used in LDAP.'''
        self.username = (
                self.last_name
                + self.first_name
                ).lower().replace(' ', '')[:10]

    def generate_token(self):
        dk = hmac.new(
            bytes(str(time.time()), 'UTF-8'),
            msg=bytes(str(time.time()) + self.email, 'UTF-8'),
            digestmod=hashlib.sha256
        ).digest()
        self.validation_token = base64.urlsafe_b64encode(dk).decode()

    def format_last_name(self):
        self.last_name = self.last_name.upper()

    def clean(self):
        self.generate_username()
        self.generate_token()
        self.format_last_name()
        return super(PendingUser, self).clean()

    def get_absolute_url(self):
        return reverse('accounts:registration-complete')

    def __str__(self):
        return '{first_name} {last_name} ({username})'.format(
            first_name=self.first_name,
            last_name=self.last_name,
            username=self.username,
        )


class Account(models.Model):
    """
    Account model where you can store all the information about a member.
    From an User object (which you can get easily thanks to Django), you can
    access the related Account entry by `user.account`
    """
    user = models.OneToOneField(
        User,
        verbose_name='default_user',
        on_delete=models.CASCADE,
    )


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User)

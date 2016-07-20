import hashlib
import hmac
import base64
import time
from django.db import models
from django.core.urlresolvers import reverse

""" Models definition """


class PendingUser(models.Model):
    username = models.CharField(
            max_length=10,
            unique=True)

    first_name = models.CharField("First name", max_length=25)

    last_name = models.CharField("Last name", max_length=25)

    email = models.EmailField("E-Mail", max_length=50)

    validation_token = models.CharField("Validation token", max_length=256)

    add_date = models.DateTimeField(
            "Date added",
            auto_now_add=True)

    last_modified = models.DateTimeField(
            "Last update",
            auto_now=True)

    """ Generates a proper username
        TO DO : check if the username is not aleready used in LDAP """

    def generate_username(self):
        self.username = ((self.last_name.lower()
                          + self.first_name.lower())[:10])

    def generate_token(self):
        dk = hmac.new(bytes(str(time.time()), 'UTF-8'),
                      msg=bytes((str(time.time()) + self.email), 'UTF-8'),
                      digestmod=hashlib.sha256).digest()
        self.validation_token = base64.b64encode(dk).decode()

    def format_last_name(self):
        self.last_name = self.last_name.upper()

    def get_absolute_url(self):
        return reverse('accounts:registration-complete')

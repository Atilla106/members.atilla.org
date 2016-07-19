import hashlib, binascii
from django.db import models
from django.core.exceptions import ValidationError


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
        self.username = (self.firstName.lower() + lastName.lower()).substring(0, 10)

    def generate_token(self):
        self.validation_token = binascii.hexlify(hashlib.pbkdf2_hmac('sha256', time.time(),
                                                self.email, 100000))



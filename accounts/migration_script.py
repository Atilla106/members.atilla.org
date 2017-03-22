"""
Creates accounts entries for all existing users.
"""

from accounts.models import Account
from django.contrib.auth.models import User


for user in User.objects.all():
    a = Account.objects.create(user=user)

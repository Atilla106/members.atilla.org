from django.db import models
from accounts.models import Account


class CleaningRoster(models.Model):
    """
    Model representing a randomly-selected roster for the room's cleaning
    """

    # Date where the people were selected
    date = models.DateField(auto_now_add=True)

    cleaners = models.ManyToManyField(Account)

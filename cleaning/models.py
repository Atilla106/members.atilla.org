from datetime import date

from django.db import models
from accounts.models import Account


class CleaningRoster(models.Model):
    """
    Model representing a randomly-selected roster for the room's cleaning
    """

    # Date where the people were selected
    date = models.DateField(auto_now_add=True)

    cleaners = models.ManyToManyField(Account)

    def save(self, *args, **kwargs):
        CleaningRoster.objects.filter(date=date.today()).delete()
        return super(CleaningRoster, self).save(*args, **kwargs)

    def __str__(self):
        return "Ménage du %s" % self.date

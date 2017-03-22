from random import sample

from django.core.management.base import BaseCommand

from accounts.models import Account
from cleaning.models import CleaningRoster


class Command(BaseCommand):
    help = 'Randomly draws three people to clean the room'

    def handle(self, *args, **options):
        volunteers = list(Account.objects.filter(cleaning=True))

        try:
            cleaners = sample(volunteers, 3)
            roster = CleaningRoster()
            roster.save()
            for cleaner in cleaners:
                roster.cleaners.add(cleaner)
        except ValueError:
            print("Not enough colunteers for cleaning")

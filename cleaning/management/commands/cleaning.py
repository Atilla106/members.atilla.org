from random import sample

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.template import loader

from accounts.models import Account
from cleaning.models import CleaningRoster


class Command(BaseCommand):
    help = 'Randomly draws three people to clean the room'

    def render_mail_content(self, cleaners, current_user):
        template = loader.get_template('cleaning/notification_mail.html')

        context = {
            'user': current_user,
            'cleaners': cleaners,
        }

        return template.render(context)

    def send_notification_mail(self, roster):
        cleaners = roster.cleaners.all()
        for current_user in cleaners:
            send_mail(
                'Ménage de la salle CY106',
                self.render_mail_content(cleaners, current_user.user),
                settings.MAIL_SENDER,
                [current_user.user.email]
            )

    def handle(self, *args, **options):
        volunteers = list(Account.objects.filter(cleaning=True))

        try:
            cleaners = sample(volunteers, 3)
            roster = CleaningRoster()
            roster.save()
            for cleaner in cleaners:
                roster.cleaners.add(cleaner)

            self.send_notification_mail(roster)
        except ValueError:
            print("Not enough volunteers for cleaning")

from django.db.utils import IntegrityError
from django.test import TestCase

from .models import PendingUser


class PendingUserTestCase(TestCase):
    def setUp(self):
        self.test1 = PendingUser.objects.create(
            first_name='Nesim',
            last_name='Fintz',
            email='contact@nf.eisti.fr',
        )

    def test_multiple_usernames(self):
        with self.assertRaises(IntegrityError):
            PendingUser.objects.create(
                first_name='Nesim',
                last_name='Fintz',
                email='contact2@nf.eisti.fr',
            )

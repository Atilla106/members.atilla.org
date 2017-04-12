from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.models import Account
from constance.test import override_config


@override_config(AUTO_ALLOW_FLAG="True")
class AccountModelTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="test", password="test")
        self.user.email = "test@eisti.fr"
        self.user.backend = 'django.contrib.auth.backends.ModelBackend'
        self.user.save()

    def test_account_model_has_user_field(self):
        account = Account(user=self.user)
        self.assertTrue(hasattr(account, 'user'))

    def test_account_model_is_created_when_user_is_created(self):
        self.assertIsNotNone(Account.objects.get(user=self.user))

    def test_user_model_has_related_account(self):
        self.assertIsNotNone(self.user.account)

    def test_user_has_perms_when_flag_true(self):
        self.assertTrue(self.user.has_perm(
                'network.can_publish_device'))

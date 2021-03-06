from django.test import TestCase
from mockldap import MockLdap

from ..ldap.actions import LDAPAccountAdder
from ..ldap.actions import LDAPAccountUpdater
from ..ldap import utils
from ..models import PendingUser


class LDAPFunctionsTestCase(TestCase):
    """
    Warning : you must update your project settings in order to pass those
    tests : the described LDAP configuration in this class may not match your
    own config.
    """

    def setUp(self):
        root = ('dc=org', {'dc': ['org']})
        top = ('dc=atilla,dc=org', {'dc': ['atilla']})
        users = ('ou=users,dc=atilla,dc=org', {'ou': ['users']})

        manager = (
                'cn=admin,dc=atilla,dc=org', {
                    'cn': ['admin'],
                    'userPassword': ['123456']})
        user1 = (
                'cn=Test USER,ou=users,dc=atilla,dc=org', {
                    'cn': ['Test USER'],
                    'uid': ['usertest'],
                    'userPassword': ['We love HDM !']})

        self.directory = dict([root, top, users, manager, user1])

        self.mockldap = MockLdap(self.directory)
        self.mockldap.start()
        self.ldap = self.mockldap['ldap://127.0.0.1']

    def tearDown(self):
        self.mockldap.stop()
        del self.ldap

    # Tests for high-level functions
    def test_user_bind(self):
        self.assertTrue(
                utils.test_user_bind(
                    'cn=Test User,ou=users,dc=atilla,dc=org',
                    'We love HDM !',
                    self.ldap))

    def test_user_migration(self):
        # First, create a pending user
        user = PendingUser(
                username='randomuser',
                first_name='Random',
                last_name='User',
                email='random.user@example.org',
                validation_token='42')

        password = 'We love HDM !'

        # Migrate this user to the LDAP
        result = LDAPAccountAdder(self.ldap).add(user, password)

        self.assertTrue(result)
        self.assertEquals(
                self.ldap.methods_called(),
                ['search', 'result', 'search_s', 'add_s'])

    def test_duplicate_user_cn_migration(self):
        # Create a duplicate user from Test User
        user = PendingUser(
                username='anothertestuser',
                first_name='Test',
                last_name='User',
                email='random.user@example.org',
                validation_token='42')

        password = 'We love HDM !'

        # Migrate this user to the LDAP
        result = LDAPAccountAdder(self.ldap).add(user, password)

        self.assertFalse(result)

    def test_duplicate_user_uid_migration(self):
        # Create a duplicate user from Test User
        user = PendingUser(
                username='usertest',
                first_name='Another',
                last_name='User',
                email='random.user@example.org',
                validation_token='42')

        password = 'We love HDM !'

        # Migrate this user to the LDAP
        result = LDAPAccountAdder(self.ldap).add(user, password)

        self.assertFalse(result)

    def test_user_password_update(self):
        account_updater = LDAPAccountUpdater('cn=Test User,ou=users,dc=atilla,dc=org')
        account_updater.change_password('We love HDM !', 'Caniche', self.ldap)

        self.assertEquals(
                self.ldap.methods_called(),
                ['simple_bind_s', 'modify_s', 'unbind_s'])

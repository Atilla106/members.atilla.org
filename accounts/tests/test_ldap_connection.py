from django.test import TestCase
from mockldap import MockLdap

from ..ldap import migration
from ..ldap import utils
from ..models import PendingUser


class LDAPConnectionTestCase(TestCase):
    ''' Warning : you must update your project settings in order to pass those
    tests : the described LDAP configuration in this class may not match your
    own config '''

    def setUp(self):
        root = ('dc=org', {'dc': ['org']})
        top = ('dc=atilla,dc=org', {'dc': ['atilla']})
        users = ('ou=users,dc=atilla,dc=org', {'ou': ['users']})

        manager = (
                'cn=admin,dc=atilla,dc=org', {
                    'cn': ['admin'],
                    'userPassword': ['123456']})
        user1 = (
                'cn=Test User,ou=users,dc=atilla,dc=org', {
                    'cn': ['Test User'],
                    'uid': ['usertest'],
                    'userPassword': ['We love HDM !']})

        self.directory = dict([root, top, users, manager, user1, user2])

        self.mockldap = MockLdap(self.directory)
        self.mockldap.start()
        self.ldap = self.mockldap['ldap://127.0.0.1']

    def tearDown(self):
        self.mockldap.stop()
        del self.ldap

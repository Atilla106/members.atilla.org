from django.test import TestCase

from mockldap import MockLdap


class LDAPConnectinTestCase(TestCase):
    def setUp(self):
        root = ('dc=org', {'dc': ['org']})
        top = ('dc=atilla,dc=org', {'dc': ['atilla']})
        users = ('ou=users,dc=atilla,dc=org', {'ou': ['users']})

        manager = (
                'cn=manager,dc=atilla,dc=org', {
                    'cn': ['manager'],
                    'userPassword': ['123456']})
        user1 = (
                'cn=Test User,ou=users,dc=atilla,dc=org', {
                    'cn': ['Test User'],
                    'uid': ['usertest'],
                    'userPassword': ['We love HDM !']})
        user2 = (
                'cn=Test User2,ou=users,dc=atilla,dc=org', {
                    'cn': ['Test User2'],
                    'uid': ['usertest2'],
                    'userPassword': ['We love HDM !']})

        self.directory = dict([root, top, users, manager, user1, user2])

        self.mockldap = MockLdap(self.directory)
        self.mockldap.start()
        self.ldap = self.mockldap['ldap://127.0.0.1']

    def tearDown(self):
        self.mockldap.stop()
        del self.ldap

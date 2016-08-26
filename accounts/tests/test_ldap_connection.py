import ldap

from django.test import TestCase
from mockldap import MockLdap

from ..ldap.connection import generic


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

        self.directory = dict([root, top, users, manager, user1])

        self.mockldap = MockLdap(self.directory)
        self.mockldap.start()
        self.ldap = self.mockldap['ldap://127.0.0.1']

        self.ldap.search.seed(
                'ou=users,dc=atilla,dc=org',
                ldap.SCOPE_SUBTREE,
                '(cn=*)',
                ['uid'])([user1])

    def tearDown(self):
        self.mockldap.stop()
        del self.ldap

    def get_generic_manager_connection(self):
        return generic.LDAPGenericConnection(
                'ldap://127.0.0.1',
                bind_dn='cn=admin,dc=atilla,dc=org',
                bind_password='123456',
                connection=self.ldap)

    def test_generic_no_bind_on_init(self):
        generic.LDAPGenericConnection(
                'ldap://127.0.0.1',
                connection=self.ldap)

        self.assertEquals(self.ldap.methods_called(), ['unbind_s'])

    def test_generic_bind_on_init(self):
        self.get_generic_manager_connection()

        self.assertEquals(self.ldap.methods_called(), [
            'simple_bind_s',
            'unbind_s'])

    def test_generic_search(self):
        c = self.get_generic_manager_connection()

        c.search(
                'ou=users,dc=atilla,dc=org',
                ldap.SCOPE_SUBTREE,
                '(cn=*)',
                ['uid'])

        self.assertEquals(self.ldap.methods_called(), [
            'simple_bind_s',
            'search'])

    def test_generic_add(self):
        c = self.get_generic_manager_connection()

        c.add_s('cn=nothing,dc=atilla,dc=org', {})

        self.assertEquals(self.ldap.methods_called(), [
            'simple_bind_s',
            'add_s'])

    def test_generic_modify(self):
        c = self.get_generic_manager_connection()

        c.modify_s('cn=Test User,ou=users,dc=atilla,dc=org', {})

        self.assertEquals(self.ldap.methods_called(), [
            'simple_bind_s',
            'modify_s'])

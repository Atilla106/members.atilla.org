# Codecs and translitcodec are needed when calling encode() methods
import codecs # noqa
import ldap
import ldap.modlist as modlist
import translitcodec # noqa

from django.conf import settings

from .connection.generic import LDAPGenericConnection
from .connection.LDAPManager import LDAPManagerConnection
from .utils import generate_crypt_password


class LDAPAccountAdder:
    """Allow the insertion of new accounts in an LDAP directory using the standard POSIX user scheme."""

    def __init__(self, connection=None):
        if connection:
            self.__connection = connection
        else:
            self.__connection = LDAPManagerConnection()

    def build_account_attributes(self, user, password):
        """
        Generate an account attributes dict that can be used in LDAP addModList.

        Also ensure that the account attributes are correctly formatted, and generate a password hash.
        """
        attrs = {}
        attrs['cn'] = '{} {}'.format(user.first_name, user.last_name)
        attrs['uid'] = user.username
        attrs['givenName'] = user.first_name
        attrs['sn'] = user.last_name
        attrs['uidNumber'] = self.get_biggest_LDAP_uid() + 1
        attrs['gidNumber'] = settings.LDAP_DEFAULT_GID
        attrs['userPassword'] = generate_crypt_password(password)
        attrs['mail'] = user.email
        attrs['homeDirectory'] = (settings.LDAP_DEFAULT_HOME_PATH + user.username)

        # Make sure that every attribute is a ascii string
        for key, value in attrs.items():
            attrs[key] = str(value).encode('translit/one/ascii', 'replace')

        attrs['objectclass'] = [
                ('inetOrgPerson').encode('translit/one/ascii', 'replace'),
                ('posixAccount').encode('translit/one/ascii', 'replace'),
                ('top').encode('translit/one/ascii', 'replace')]

        return attrs

    def get_biggest_LDAP_uid(self):
        """Get the biggest currently registered LDAP UID."""
        search_filter = '(objectClass=posixAccount)'
        search_attribute = ["uidNumber"]
        search_scope = ldap.SCOPE_SUBTREE

        result_id = self.__connection.search(
                settings.LDAP_USERS_BASE_DN,
                search_scope,
                search_filter,
                search_attribute)

        max_uid = 0

        while 1:
            try:
                result_type, result_data = self.__connection.result(result_id, 0)
            except ldap.NO_SUCH_OBJECT:
                raise ldap.LDAPError(
                    'Distinguished name ({}) does not exist.'.format(
                        settings.LDAP_USERS_BASE_DN))

            if result_type == ldap.RES_SEARCH_ENTRY:
                try:
                    uid = int(result_data[0][1]['uidNumber'][0])
                    if uid > max_uid:
                        max_uid = uid
                except:
                    pass
            else:
                break

        return max_uid

    def test_unique(self, user_id, user_cn):
        """
        Test if the given user common name or user ID is already present in the LDAP directory.

        Return True if no such user can be found in the directory.
        """

        # As we create a byte string, we can't use format() here
        query_string = b''.join([b'(|(cn=', user_cn, b')(uid=', user_id, b'))'])

        results = self.__connection.search_s(
                settings.LDAP_USERS_BASE_DN,
                ldap.SCOPE_SUBTREE,
                query_string.decode('utf-8'))

        return (len(results) == 0)

    def add(self, pending_user, password):
        """
        Add the given user to the current LDAP directory.

        If an account having the same user name as the one of the pending_user, no action will be taken.
        Return True if the user has been successfully added.
        """
        attrs = self.build_account_attributes(pending_user, password)

        if self.test_unique(attrs['uid'], attrs['cn']):
            dn = 'cn={} {},{}'.format(
                    pending_user.first_name.encode(
                        'translit/one/ascii',
                        'replace').decode(),
                    pending_user.last_name.encode(
                        'translit/one/ascii',
                        'replace').decode(),
                    settings.LDAP_USERS_BASE_DN)

            ldif = modlist.addModlist(attrs)

            try:
                self.__connection.add_s(dn, ldif)
                return True
            except:
                return False
        else:
            return False


class LDAPAccountUpdater:
    """Perform generic actions on a given LDAP account."""

    def __init__(self, user_dn):
        self.__user_dn = user_dn

    def change_password(self, old_password, new_password, connection=None):
        """
        Update the password of a given user.

        If no LDAP connection is provided, the user old password will be used in a simple bind action.
        This allows to check if the user's old password is the correct one.

        Returns True if the password has correctly been updated.
        """

        try:
            connection = LDAPGenericConnection(
                    settings.LDAP_SERVER_URI,
                    self.__user_dn,
                    old_password,
                    connection)
        except (NameError, ldap.LDAPError):
            return False

        new_crypt_password = generate_crypt_password(new_password)
        mod_attrs = [(
                ldap.MOD_REPLACE,
                'userPassword',
                [str(new_crypt_password).encode('ascii', 'ignore')]
            )]
        connection.modify_s(self.__user_dn, mod_attrs)
        return True

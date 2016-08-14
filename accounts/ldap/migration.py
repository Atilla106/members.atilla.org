import ldap.modlist as modlist

from django.conf import settings

from .connection.LDAPManager import LDAPManagerConnection
from .utils import generate_crypt_password, get_biggest_LDAP_uid


def migrate_to_LDAP(pending_user, password, connection=None):
    password = generate_crypt_password(password)

    connection = LDAPManagerConnection(connection=connection)
    attrs = {}
    attrs['cn'] = '{} {}'.format(
            pending_user.first_name,
            pending_user.last_name)
    attrs['uid'] = pending_user.username
    attrs['givenName'] = pending_user.first_name
    attrs['sn'] = pending_user.last_name
    attrs['uidNumber'] = get_biggest_LDAP_uid(connection) + 1
    attrs['gidNumber'] = settings.LDAP_DEFAULT_GID
    attrs['userPassword'] = password
    attrs['mail'] = pending_user.email
    attrs['homeDirectory'] = (settings.LDAP_DEFAULT_HOME_PATH
                              + pending_user.username)

    # Make sure that every attribute is a ascii string
    for key, value in attrs.items():
        attrs[key] = str(value).encode('ascii', 'ignore')

    attrs['objectclass'] = [
            ('inetOrgPerson').encode('ascii', 'ignore'),
            ('posixAccount').encode('ascii', 'ignore'),
            ('top').encode('ascii', 'ignore')]

    dn = 'cn={} {},{}'.format(
            pending_user.first_name,
            pending_user.last_name,
            settings.LDAP_USERS_BASE_DN)
    ldif = modlist.addModlist(attrs)
    connection.add_s(dn, ldif)

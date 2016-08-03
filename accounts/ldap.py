import os.path

import crypt
import ldap
import ldap.modlist as modlist
from django.conf import settings


def generate_crypt_password(password):
    salt = crypt.mksalt(method=crypt.METHOD_SHA512)
    salt = '$1$' + salt + '$'
    return '{CRYPT}' + str(crypt.crypt(password, salt))


def get_biggest_LDAP_uid(connection):
    search_filter = '(objectClass=posixAccount)'
    search_attribute = ['uidNumber']
    search_scope = ldap.SCOPE_SUBTREE
    result_id = connection.search(
        settings.LDAP_USERS_BASE_DN,
        search_scope,
        search_filter,
        search_attribute,
    )

    max_uid = 0

    # JPF
    while 1:
        try:
            result_type, result_data = connection.result(result_id, 0)
        except ldap.NO_SUCH_OBJECT:
            raise ldap.LDAPError(
                'Distinguished name ({dn}) does not exist.'.format(
                    dn=settings.LDAP_USERS_BASE_DN,
                )
            )

        if result_type == ldap.RES_SEARCH_ENTRY:
            try:
                uid = int(result_data[0][1]['uidNumber'][0])
                max_uid = max(max_uid, uid)
            except:
                pass
        else:
            break

    return max_uid


def migrate_to_LDAP(pending_user, password):
    password = generate_crypt_password(password)

    # First, check the config vars
    if (
        settings.LDAP_SERVER_URI and
        settings.LDAP_MANAGEMENT_DN and
        settings.LDAP_MANAGEMENT_PASSWORD and
        settings.LDAP_DEFAULT_GID and
        settings.LDAP_USERS_BASE_DN and
        settings.LDAP_DEFAULT_USER_OU and
        settings.LDAP_DEFAULT_HOME_PATH
    ):
        connection = ldap.initialize(settings.LDAP_SERVER_URI)
        connection.bind(
            settings.LDAP_MANAGEMENT_DN,
            settings.LDAP_MANAGEMENT_PASSWORD,
        )

        attrs = {}
        attrs['cn'] = '{first_name} {last_name}'.format(
            first_name=pending_user.first_name,
            last_name=pending_user.last_name,
        )

        attrs['uid'] = pending_user.username
        attrs['givenName'] = pending_user.first_name
        attrs['sn'] = pending_user.last_name
        attrs['uidNumber'] = get_biggest_LDAP_uid(connection) + 1
        attrs['gidNumber'] = settings.LDAP_DEFAULT_GID
        attrs['userPassword'] = password
        attrs['mail'] = pending_user.email
        attrs['homeDirectory'] = os.path.join(
            settings.LDAP_DEFAULT_HOME_PATH,
            pending_user.username,
        )

        # Make sure that every attribute is a ascii string
        for key, value in attrs.items():
            attrs[key] = str(value).encode('ascii', 'ignore')

        attrs['objectclass'] = [
            ('inetOrgPerson').encode('ascii', 'ignore'),
            ('posixAccount').encode('ascii', 'ignore'),
            ('top').encode('ascii', 'ignore'),
        ]

        dn = 'cn={first_name} {last_name},{base_dn}'.format(
            first_name=pending_user.first_name,
            last_name=pending_user.last_name,
            base_dn=settings.LDAP_USERS_BASE_DN,
        )

        ldif = modlist.addModlist(attrs)
        connection.add_s(dn, ldif)
        connection.unbind_s()

    else:
        raise NameError('LDAP settings not properly configured')

import crypt
import ldap

from django.conf import settings


def generate_crypt_password(password):
    salt = crypt.mksalt(method=crypt.METHOD_SHA512)
    salt = '$1${}$'.format(salt)
    return '{CRYPT}{}'.format(str(crypt.crypt(password, salt)))


def get_biggest_LDAP_uid(connection):
    search_filter = '(objectClass=posixAccount)'
    search_attribute = ["uidNumber"]
    search_scope = ldap.SCOPE_SUBTREE

    result_id = connection.search(
            settings.LDAP_USERS_BASE_DN,
            search_scope,
            search_filter,
            search_attribute)

    max_uid = 0
    # JPF
    while 1:
        try:
            result_type, result_data = connection.result(result_id, 0)
        except ldap.NO_SUCH_OBJECT:
            raise ldap.LDAPError(
                "Distinguished name (%s) does not exist."
                % settings.LDAP_USERS_BASE_DN)

        if result_type == ldap.RES_SEARCH_ENTRY:
            try:
                uid = int(result_data[0][1]['uidNumber'][0])
                if (uid > max_uid):
                    max_uid = uid
            except:
                pass
        else:
            break

    return max_uid

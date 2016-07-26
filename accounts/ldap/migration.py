import ldap
import ldap.modlist as modlist
import string

from django.conf import settings

from .connection.LDAPManager import LDAPManagerConnection
from .utils import *

def get_biggest_LDAP_uid(connection):
    search_filter = '(objectClass=posixAccount)'
    search_attribute = ["uidNumber"]
    search_scope = ldap.SCOPE_SUBTREE
    print("Trace1A")
    print(connection)
    result_id = connection.search(settings.LDAP_USERS_BASE_DN,
                                  search_scope, search_filter,
                                  search_attribute)
    print("Trace1B")
    max_uid = 0

    # JPF
    while 1:
        try:
            result_type, result_data = connection.result(result_id, 0)
        except ldap.NO_SUCH_OBJECT:
            raise ldap.LDAPError("Distinguished name (%s) does not exist."
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

def migrate_to_LDAP(pending_user, password):
    password = generate_crypt_password(password)

    connection = LDAPManagerConnection()
    print(connection)
    print("Trace1")
    attrs = {}
    attrs['cn'] = (pending_user.first_name
                   + " " + pending_user.last_name)
    attrs['uid'] = pending_user.username
    attrs['givenName'] = pending_user.first_name
    attrs['sn'] = pending_user.last_name
    attrs['uidNumber'] = get_biggest_LDAP_uid(connection) + 1
    attrs['gidNumber'] = settings.LDAP_DEFAULT_GID
    attrs['userPassword'] = password
    attrs['mail'] = pending_user.email
    attrs['homeDirectory'] = (settings.LDAP_DEFAULT_HOME_PATH
                              + pending_user.username)

    print("Trace2")
    # Make sure that every attribute is a ascii string
    for key, value in attrs.items():
        attrs[key] = str(value).encode('ascii', 'ignore')

    attrs['objectclass'] = [('inetOrgPerson').encode('ascii', 'ignore'),
                            ('posixAccount').encode('ascii', 'ignore'),
                            ('top').encode('ascii', 'ignore')]

    dn = ("cn=" + pending_user.first_name + " " + pending_user.last_name
          + "," + settings.LDAP_USERS_BASE_DN)
    ldif = modlist.addModlist(attrs)
    print("Trace3")
    connection.add_s(dn, ldif)

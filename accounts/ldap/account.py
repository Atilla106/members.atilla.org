import ldap
import ldap.modlist as modlist
import crypt
import random
import string

from django.conf import settings

from .utils import check_LDAP_configuration

class LDAPAccount():

    def __init__(self, user_dn):
        check_LDAP_configuration()
        self.connection = LDAPManagerConnection().get_connection()

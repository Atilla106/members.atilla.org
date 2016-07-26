import ldap
import ldap.modlist as modlist
import crypt
import random
import string

from django.conf import settings

from .utils import generate_crypt_password
from .connection.LDAPManager import LDAPManagerConnection

class LDAPAccount():

    def __init__(self, user_dn):
        self.connection = LDAPManager().get_connection()
        self.user_dn = user_dn

    def change_password(self, new_password):
        new_password = generate_crypt_password(new_password)
        mod_attrs = [(ldap.MOD_REPLACE, 'userPassword',
                      new_password.encode('ascii', 'ignore'))]
        self.connection.modify_s(self.user_dn, mod_attrs)

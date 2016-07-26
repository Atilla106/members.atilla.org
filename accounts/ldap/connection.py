import ldap
import ldap.modlist as modlist
import crypt
import random
import string

from django.conf import settings

from .utils import check_LDAP_configuration

class LDAPManagerConnection():

    def __init__(self):
        check_LDAP_configuration()
        self.connection = ldap.initialize(settings.LDAP_SERVER_URI)
        self.connection.bind(settings.LDAP_MANAGEMENT_DN,
                             settings.LDAP_MANAGEMENT_PASSWORD)

    def get_connection():
        return self.connection

    def __del__(self):
        self.connection.unbind_s()

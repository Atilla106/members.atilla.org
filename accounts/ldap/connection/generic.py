import ldap

from django.conf import settings


class LDAPGenericConnection():
    def __init__(self, server_uri, bind_dn=None, bind_password=None):
        self.check_LDAP_configuration()
        self.connection = ldap.initialize(server_uri)

        if bind_dn is not None and bind_password is not None:
            self.bind(bind_dn, bind_password)

    def check_LDAP_configuration(self):
        if (not settings.LDAP_SERVER_URI
                or not settings.LDAP_MANAGEMENT_DN
                or not settings.LDAP_MANAGEMENT_PASSWORD
                or not settings.LDAP_DEFAULT_GID
                or not settings.LDAP_USERS_BASE_DN
                or not settings.LDAP_DEFAULT_USER_OU
                or not settings.LDAP_DEFAULT_HOME_PATH):
            raise NameError("LDAP settings not properly configured")

    def bind(self, bind_dn, bind_password):
        self.connection.bind(bind_dn, bind_password)

    def search(self, base_dn, search_scope, search_filter, search_attribute):
        return self.connection.search(
                base_dn,
                search_scope,
                search_filter,
                search_attribute)

    def result(self, result_id, result_all):
        return self.connection.result(result_id, result_all)

    def add_s(self, dn, ldif):
        return self.connection.add_s(dn, ldif)

    def get_connection(self):
        return self.connection

    def __del__(self):
        self.connection.unbind_s()

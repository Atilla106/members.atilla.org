import ldap

from django.conf import settings


class LDAPGenericConnection():
    """
    Handler for LDAP connections.

    Define a set of methods that aim to ease LDAP requests with the application.
    """

    def __init__(
            self,
            server_uri,
            bind_dn=None,
            bind_password=None,
            connection=None):
        """
        Initialize a new LDAP connection using the given parameters.

        Throws NameError if the project settings are not properly configured.
        Throws ldap.LDAPError if the connection to the LDAP directory is not successful.
        """
        self.check_LDAP_configuration()

        if connection is None:
            self.connection = ldap.initialize(server_uri)
        else:
            self.connection = connection

        if bind_dn is not None and bind_password is not None:
            self.bind(bind_dn, bind_password)

    def check_LDAP_configuration(self):
        """Ensure that the LDAP settings of the project are correctly defined."""
        if (not settings.LDAP_SERVER_URI
                or not settings.LDAP_MANAGEMENT_DN
                or not settings.LDAP_MANAGEMENT_PASSWORD
                or not settings.LDAP_DEFAULT_GID
                or not settings.LDAP_USERS_BASE_DN
                or not settings.LDAP_DEFAULT_USER_OU
                or not settings.LDAP_DEFAULT_HOME_PATH):
            raise NameError('LDAP settings not properly configured')

    def bind(self, bind_dn, bind_password):
        self.connection.simple_bind_s(bind_dn, bind_password)

    def search(self, base_dn, search_scope, search_filter, search_attribute):
        return self.connection.search(
                base_dn,
                search_scope,
                search_filter,
                search_attribute)

    def search_s(self, base_dn, search_scope, search_attribute):
        return self.connection.search_s(
                base_dn,
                search_scope,
                search_attribute)

    def result(self, result_id, result_all):
        return self.connection.result(result_id, result_all)

    def add_s(self, dn, ldif):
        return self.connection.add_s(dn, ldif)

    def modify_s(self, dn, ldif):
        return self.connection.modify_s(dn, ldif)

    def get_connection(self):
        return self.connection

    def __del__(self):
        """Close the connection to the LDAP directory when the object is destroyed."""
        self.connection.unbind_s()

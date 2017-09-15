from django.conf import settings

from .generic import LDAPGenericConnection


class LDAPManagerConnection(LDAPGenericConnection):
    """
    Provide a connection to an LDAP server using manager credentials taken from the project configuration.

    Inherits from LDAPGenericConnection.
    """

    def __init__(self, connection=None):
        super(LDAPManagerConnection, self).__init__(
            settings.LDAP_SERVER_URI,
            settings.LDAP_MANAGEMENT_DN,
            settings.LDAP_MANAGEMENT_PASSWORD,
            connection)

"""Provide a set of useful functions for LDAP related low level operations."""
import crypt
import ldap

from django.conf import settings

from .connection.generic import LDAPGenericConnection


def generate_crypt_password(password):
    """Generate a salted hash from the password given in parameter."""
    salt = crypt.mksalt(method=crypt.METHOD_SHA512)
    salt = '$1${}$'.format(salt)
    return '{{CRYPT}}{}'.format(str(crypt.crypt(password, salt)))


def test_user_bind(user_dn, password, connection=None):
    """Using the given user and password, try to establish a connection to an LDAP server."""
    try:
        LDAPGenericConnection(settings.LDAP_SERVER_URI, user_dn, password, connection)
        return True
    except (NameError, ldap.LDAPError):
        return False

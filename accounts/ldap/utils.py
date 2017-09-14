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


def test_user_bind(user_dn, password, server_uri=None):
    """
    Using the given user and password, try to establish a connection to an LDAP server.

    If no `server_uri` is provided, use the default LDAP_SERVER_URI from the project configuration.
    Return True if the connection is successful.
    """
    try:
        LDAPGenericConnection(
                (server_uri if server_uri is not None else settings.LDAP_SERVER_URI),
                user_dn,
                password)
        return True
    except (NameError, ldap.LDAPError):
        return False


def change_user_password(user_dn, old_password, new_password, connection=None):
    try:
        connection = LDAPGenericConnection(
                settings.LDAP_SERVER_URI,
                user_dn,
                old_password,
                connection)
    except (NameError, ldap.LDAPError):
        return False

    new_crypt_password = generate_crypt_password(new_password)
    mod_attrs = [(
        ldap.MOD_REPLACE,
        'userPassword',
        [str(new_crypt_password).encode('ascii', 'ignore')]
        )]
    connection.modify_s(user_dn, mod_attrs)
    return True

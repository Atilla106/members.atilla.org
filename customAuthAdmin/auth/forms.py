from django.contrib.auth.forms import (
    ReadOnlyPasswordHashField,
    ReadOnlyPasswordHashWidget,
    UserChangeForm
)

from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX

from django.utils.translation import ugettext_lazy as _


class CustomReadOnlyPasswordHashWidget(ReadOnlyPasswordHashWidget):
    """
    When a user gets his account on the platform from an LDAP server, the password associated
    with the account will be left as "unusable" in the database. This is made so that the django-ldap
    module tries to authenticate the user from the LDAP, and not from the platform user database.

    New administrators of the platform can sometimes think that changing the password in the admin will
    change the password on the LDAP server, which is not implemented. As such, this class adds
    a simple warning message around the password field in order to indicate that if the user comes from
    an LDAP server, its password should probably be changed on the LDAP, and not here.
    """

    def get_context(self, name, value, attrs):
        context = super(CustomReadOnlyPasswordHashWidget, self).get_context(name, value, attrs)

        if not value or value.startswith(UNUSABLE_PASSWORD_PREFIX):
            context['summary'].append({'label': (
                "ATTENTION: Ce mot de passe peut-être géré par l'annuaire LDAP. "
                "Dans ce cas, la modification du mot de passe via le formulaire ci-après ne sera pas effective "
                "sur l'ensemble des services de l'association."
            )})

        return context


class CustomReadOnlyPasswordHashField(ReadOnlyPasswordHashField):
    widget = CustomReadOnlyPasswordHashWidget


class CustomUserChangeForm(UserChangeForm):
    """Simple override of the UserChangeForm in order to inject our CustomReadOnlyPasswordHashField."""

    password = CustomReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            "Raw passwords are not stored, so there is no way to see this "
            "user's password, but you can change the password using "
            "<a href=\"../password/\">this form</a>."
        )
    )

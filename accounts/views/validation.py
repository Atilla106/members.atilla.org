from django import forms
from django.forms import ValidationError
from django.views import generic
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse_lazy

from ..models import PendingUser
from ..ldap.migration import migrate_to_LDAP


class ValidateRegistrationForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())
    password_conf = forms.CharField(widget=forms.PasswordInput())

""" Try to find the DB entry corresponding to the given token
    if one entry is found, ask for a password and sync the account
    with the LDAP """


class ValidateRegistrationView(generic.FormView):
    template_name = 'accounts/finish_validation.html'
    form_class = ValidateRegistrationForm
    success_url = reverse_lazy('accounts:validation-complete')

    def load_pending_user(self, token):
        self.pending_user = get_object_or_404(PendingUser,
                                              validation_token=token)

    def get(self, *args, **kwargs):
        self.load_pending_user(kwargs['token'])
        return super(ValidateRegistrationView, self).get(self, *args, **kwargs)

    def form_valid(self, form):
        self.load_pending_user(self.kwargs['token'])
        if (form.cleaned_data['password'] !=
                form.cleaned_data['password_conf']):
            raise ValidationError('The passwords are not the same',
                                  code='invalid')
        else:
            migrate_to_LDAP(self.pending_user,
                                 form.cleaned_data['password'])
            self.pending_user.delete()
            return super(ValidateRegistrationView, self).form_valid(form)


class ValidationCompleteView(generic.TemplateView):
    template_name = 'accounts/validation_complete.html'

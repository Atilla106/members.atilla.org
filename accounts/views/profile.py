from django import forms
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ValidationError
from django.views import generic

from ..ldap.utils import test_user_bind
from ..ldap.utils import change_user_password


class UpdatePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput())
    new_password_conf = forms.CharField(widget=forms.PasswordInput())


class UpdatePasswordView(LoginRequiredMixin, generic.FormView):
    template_name = 'accounts/update_password.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('accounts:change_password')

    def form_valid(self, form):
        old_password = form.cleaned_data['old_password']
        new_password = form.cleaned_data['new_password']
        new_password_conf = form.cleaned_data['new_password_conf']

        if not test_user_bind(
                self.request.user.dn,
                old_password):
            raise ValidationError(
                    'The old password is incorrect',
                    code='invalid'
                    )
        elif new_password != new_password_conf:
            raise ValidationError(
                    'Passwords are not the same',
                    code='invalid'
                    )
        else:
            change_user_password(
                    self.request.user.dn,
                    old_password,
                    new_password)
            return super(ValidateRegistrationView, self).form_valid(form)

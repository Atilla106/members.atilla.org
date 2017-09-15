from django import forms
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.views.generic.edit import UpdateView

from ..ldap.utils import test_user_bind
from ..ldap.utils import change_user_password
from ..models import Account


class UpdatePasswordForm(forms.Form):
    old_password = forms.CharField(
            widget=forms.PasswordInput(),
            label='Ancien mot de passe')

    new_password = forms.CharField(
            widget=forms.PasswordInput(),
            label='Nouveau mot de passe')

    new_password_conf = forms.CharField(
            widget=forms.PasswordInput(),
            label='Confirmation du mot de passe')


class UpdatePasswordView(LoginRequiredMixin, generic.FormView):
    template_name = 'accounts/update_password.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form):
        old_password = form.cleaned_data['old_password']
        new_password = form.cleaned_data['new_password']
        new_password_conf = form.cleaned_data['new_password_conf']

        if not test_user_bind(
                self.request.user.ldap_user.dn,
                old_password):
            form.add_error(
                    'old_password',
                    'The old password is incorrect')
            return super(UpdatePasswordView, self).form_invalid(form)
        elif new_password != new_password_conf:
            form.add_error(
                    'new_password',
                    'Passwords are not the same')
            return super(UpdatePasswordView, self).form_invalid(form)
        else:
            if change_user_password(
                    self.request.user.ldap_user.dn,
                    old_password,
                    new_password):
                messages.success(self.request, 'Your password was successfully updated')
                return super(UpdatePasswordView, self).form_valid(form)
            else:
                form.add_error(
                        'old_password',
                        'Unable to perform update')
                return super(UpdatePasswordView, self).form_invalid(form)


class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = "accounts/profile.html"
    model = Account
    fields = ['cleaning']
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form):
        messages.success(self.request, 'Your cleaning preference was successfully updated')
        return super(ProfileView, self).form_valid(form)

    def get_object(self, queryset=None):
        return self.request.user.account

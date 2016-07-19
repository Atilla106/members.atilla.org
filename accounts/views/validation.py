from django.shortcuts import render
from django import forms
from django.views import generic

class ValidateRegistrationForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())
    password_conf = forms.CharField(widget=forms.PasswordInput())

""" Try to find the DB entry corresponding to the given token
    if one entry is found, ask for a password and sync the account
    with the LDAP """

class ValidateRegistrationView(generic.FormView):
    template_name = 'accounts/finish_validation.html'
    form_class = ValidateRegistrationForm

    def get(self, *args, **kwargs):
        self.pending_user = get_object_or_404(PendingUser,
                validation_token=kwargs['token'])

    def form_valid(self, form):
        if (form.cleaned_data['password'] != form.cleaned_data['password_conf']):
            raise ValidationError('The passwords are not the same')
        else:
            migrate_to_LDAP(self.pending_user, form.cleaned_data['password'])
            self.pending_user.delete()
            return super(ValidateRegistrationView, self).form_valid(form)

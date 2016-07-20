from django.shortcuts import render
from django import forms, views
from django.views import generic
from django.core.mail import send_mail
from django.template import loader

from ..settings import MAIL_SENDER
from ..models import PendingUser

class RegisterView(generic.edit.CreateView):
    template_name = 'accounts/register.html'
    model = PendingUser
    fields = ['first_name', 'last_name', 'email']

    def render_mail_content(self, pending_user):
        template = loader.get_template('accounts/validation_mail.html')

        context = {
                   'first_name': pending_user.first_name,
                   'last_name': pending_user.last_name,
                   'email': pending_user.email,
                   'validation_token': pending_user.validation_token
                }

        return template.render(context, self.request)

    """ Validate the account informations and send a confirmation mail """
    def form_valid(self, form):
        pending_user = form.save(commit=False)
        pending_user.format_last_name()
        pending_user.generate_username()
        pending_user.generate_token()
        pending_user.full_clean()

        """ Send confirmation email """
        send_mail("Account validation",
                  self.render_mail_content(pending_user),
                  MAIL_SENDER,
                  [pending_user.email])

        return super(RegisterView, self).form_valid(form)

class RegistrationCompleteView(generic.TemplateView):
    template_name = 'accounts/registration_complete.html'

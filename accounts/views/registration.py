from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader
from django.views import generic

from ..models import PendingUser


class RegisterForm(forms.ModelForm):
    agreement = forms.BooleanField(
        label='Je reconnais être membre d’ATILLA '
        'et accepte la charte des ressources '
        'informatiques de l’association'
    )

    class Meta:
        model = PendingUser
        fields = ['first_name', 'last_name', 'email']


class RegisterView(generic.edit.CreateView):
    template_name = 'accounts/register.html'
    model = PendingUser
    form_class = RegisterForm

    def render_mail_content(self, pending_user):
        template = loader.get_template('accounts/validation_mail.html')

        url_prefix = "https://" if settings.PLATFORM_USING_HTTPS else "http://"
        platform_url = (url_prefix + settings.PLATFORM_HOSTNAME)

        context = {
            'first_name': pending_user.first_name,
            'last_name': pending_user.last_name,
            'email': pending_user.email,
            'username': pending_user.username,
            'platform_url': platform_url,
            'validation_token': pending_user.validation_token,
            'PLATFORM_NAME': settings.PLATFORM_NAME,
        }

        return template.render(context, self.request)

    def form_valid(self, form):
        """Validate the account informations and send a confirmation mail."""
        pending_user = form.save(commit=False)

        # Send confirmation email
        send_mail(
            "Account validation",
            self.render_mail_content(pending_user),
            settings.MAIL_SENDER,
            [pending_user.email],
        )

        return super(RegisterView, self).form_valid(form)


class RegistrationCompleteView(generic.TemplateView):
    template_name = 'accounts/registration_complete.html'

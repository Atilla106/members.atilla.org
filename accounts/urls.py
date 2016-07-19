from django.conf.urls import include, url
from .views import registration, validation

app_name = "accounts"
urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    url('^register/$', registration.RegisterView.as_view(), name='register'),
    url('^validate/(?P<token>[a-zA-Z0-9]*)/',
        validation.ValidateRegistrationView.as_view(), name='validate'),
]

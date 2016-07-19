from django.conf.urls import include, url
from .views import registration, validation

app_name = "accounts"
urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    url('^register/$', registration.RegisterView.as_view(), name='register'),
    url('^register/complete/$',
        registration.RegistrationCompleteView.as_view(),
        name='registration-complete'),
    url('^validate/(?P<token>.*)',
        validation.ValidateRegistrationView.as_view(),
        name='validate'),
]

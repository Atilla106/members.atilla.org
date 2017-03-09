from django.conf.urls import url
from django.contrib.auth import views as auth_views
from .views import registration, validation, profile

app_name = "accounts"
urlpatterns = [
    url('^login/$', auth_views.login, name='login'),
    url('^logout/$', auth_views.logout, name='logout'),
    url('^register/$', registration.RegisterView.as_view(), name='register'),
    url('^register/complete/$',
        registration.RegistrationCompleteView.as_view(),
        name='registration-complete'),
    url('^validate/complete/$',
        validation.ValidationCompleteView.as_view(),
        name='validation-complete'),
    url('^validate/token/(?P<token>.*)',
        validation.ValidateRegistrationView.as_view(),
        name='validate'),
    url('^password/update/$',
        profile.UpdatePasswordView.as_view(),
        name='change_password'),
]

from django.conf.urls import include, url

from . import views

urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
]

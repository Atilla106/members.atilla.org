from django.conf.urls import url
from . import views
app_name = "cleaning"
urlpatterns = [
    url('^', views.portal_view, name="portal"),
]

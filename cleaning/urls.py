from django.conf.urls import url
from .views import portalView
app_name = "cleaning"
urlpatterns = [
    url('^', portalView, name="portal")
]

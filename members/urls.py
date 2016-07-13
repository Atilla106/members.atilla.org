from django.conf.urls import include, url
from django.contrib import admin

from network.views import device

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^network/', include('network.urls')),
    url(r'^$', device.DeviceView.as_view())
]

from django.conf.urls import include, url
from django.contrib import admin

from network.views import device
from members.views import legal_view

urlpatterns = [
    url(r'^legal$', legal_view, name="legal"),
    url(r'^admin/', admin.site.urls),
    url(
        r'^accounts/',
        include('accounts.urls', namespace='accounts'),
    ),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^network/', include('network.urls')),
    url(r'^cleaning/', include('cleaning.urls')),
    url(r'^ethernet/', include('ethernet_auth.urls')),
    url(r'^$', device.DeviceView.as_view(), name="portal")
]

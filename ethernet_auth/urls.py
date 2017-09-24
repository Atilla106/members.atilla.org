from django.conf.urls import url

from .views import SwitchPortView
from .views import SwitchPortDetailView
from .views import SwitchPortActionCreateView

app_name = 'ethernet_auth'

urlpatterns = [
    url(r'^switches/ports/$', SwitchPortView.as_view(), name='switch_port_list'),
    url(r'^switches/ports/(?P<pk>[0-9]+)/$', SwitchPortDetailView.as_view(), name='switch_port_detail'),
    url(r'^switches/ports/(?P<pk>[0-9]+)/actions/add/$', SwitchPortActionCreateView.as_view(),
        name='switch_port_action_create')
]

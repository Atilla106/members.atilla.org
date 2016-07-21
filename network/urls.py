from django.conf.urls import url

from .views import device, interface, render

app_name = 'network'

urlpatterns = [
        url(r'^devices/$',
            device.DeviceView.as_view(),
            name='index'),
        url(r'^devices/add/$',
            device.DeviceCreateView.as_view(),
            name='device_create'),
        url(r'^devices/(?P<pk>[0-9]+)/$',
            device.DeviceDetailView.as_view(),
            name='device_detail'),
        url(r'^devices/(?P<pk>[0-9]+)/edit/$',
            device.DeviceUpdateView.as_view(),
            name='device_update'),
        url(r'^devices/(?P<pk>[0-9]+)/delete/$',
            device.DeviceDeleteView.as_view(),
            name='device_delete'),

        url(r'^devices/(?P<pk>[0-9]+)/interfaces/add/$',
            interface.InterfaceCreateView.as_view(),
            name='interface_create'),
        url(r'^devices/(?P<pk1>[0-9]+)/interfaces/(?P<pk2>[0-9]+)/edit/$',
            interface.InterfaceUpdateView.as_view(),
            name='interface_update'),
        url(r'^devices/(?P<pk1>[0-9]+)/interfaces/(?P<pk2>[0-9]+)/delete/$',
            interface.InterfaceDeleteView.as_view(),
            name='interface_delete'),

        url(r'^render/dhcp/$',
            render.RenderDHCPView.as_view(),
            name='render_DHCP'),
        url(r'^render/dns/$',
            render.RenderDNSView.as_view(),
            name='render_DNS'),
        url(r'^render/dns/reverse/$',
            render.RenderReverseDNSView.as_view(),
            name='render_reverse_DNS'),

]

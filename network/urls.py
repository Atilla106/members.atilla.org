from django.conf.urls import url

from .views import device, interface, render

app_name = 'network'

urlpatterns = [
        url(r'^devices/$',
            device.DeviceView.as_view(),
            name='index'),
        url(r'^devices/add/$',
            device.DeviceCreateView.as_view(),
            name='deviceCreate'),
        url(r'^devices/(?P<pk>[0-9]+)/$',
            device.DeviceDetailView.as_view(),
            name='deviceDetail'),
        url(r'^devices/(?P<pk>[0-9]+)/edit/$',
            device.DeviceUpdateView.as_view(),
            name='deviceUpdate'),
        url(r'^devices/(?P<pk>[0-9]+)/delete/$',
            device.DeviceDeleteView.as_view(),
            name='deviceDelete'),

        url(r'^devices/(?P<pk>[0-9]+)/interfaces/add/$',
            interface.InterfaceCreateView.as_view(),
            name='interfaceCreate'),
        url(r'^devices/(?P<pk1>[0-9]+)/interfaces/(?P<pk2>[0-9]+)/edit/$',
            interface.InterfaceUpdateView.as_view(),
            name='interfaceUpdate'),
        url(r'^devices/(?P<pk1>[0-9]+)/interfaces/(?P<pk2>[0-9]+)/delete/$',
            interface.InterfaceDeleteView.as_view(),
            name='interfaceDelete'),

        url(r'^render/dhcp/$',
            render.RenderDHCPView.as_view(),
            name='renderDHCP'),
        url(r'^render/dns/$',
            render.RenderDNSView.as_view(),
            name='renderDNS'),
        url(r'^render/dns/reverse/$',
            render.RenderReverseDNSView.as_view(),
            name='renderReverseDNS'),

]

from django.conf.urls import url

from . import views

app_name = 'network'

urlpatterns = [
        url(r'^devices/$',
            views.DeviceView.as_view(),
            name='index'),
        url(r'^devices/add/$',
            views.DeviceCreateView.as_view(),
            name='deviceCreate'),
        url(r'^devices/(?P<pk>[0-9]+)/$',
            views.DeviceDetailView.as_view(),
            name='deviceDetail'),
        url(r'^devices/(?P<pk>[0-9]+)/edit/$',
            views.DeviceUpdateView.as_view(),
            name='deviceUpdate'),
        url(r'^devices/(?P<pk>[0-9]+)/delete/$',
            views.DeviceDeleteView.as_view(),
            name='deviceDelete'),

        url(r'^devices/(?P<pk>[0-9]+)/interfaces/add/$',
            views.InterfaceCreateView.as_view(),
            name='interfaceCreate'),
        url(r'^devices/(?P<pk1>[0-9]+)/interfaces/(?P<pk2>[0-9]+)/edit/$',
            views.InterfaceUpdateView.as_view(),
            name='interfaceUpdate'),
        url(r'^devices/(?P<pk1>[0-9]+)/interfaces/(?P<pk2>[0-9]+)/delete/$',
            views.InterfaceDeleteView.as_view(),
            name='interfaceDelete'),
]

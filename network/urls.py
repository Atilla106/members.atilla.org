"""url(r'^devices/(?P<pk>[0-9]+)/$',
            views.DeviceDetailView.as_view(),
            name='deviceDetail'),
        url(r'^devices/(?P<pk>[0-9]+)/edit/$',
            views.DeviceEditView.as_view(),
            name='deviceEdit'),
        url(r'^devices/add/$',
            views.DeviceAddView, name='deviceAdd'),"""
from django.conf.urls import url

from . import views

app_name = 'network'

urlpatterns = [
        url(r'^devices/$',
            views.DeviceView.as_view(),
            name='index'),
]

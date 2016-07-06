from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from .models import Device, Interface

class DeviceView(LoginRequiredMixin, generic.ListView):
    template_name = 'network/devices.html'
    context_object_name = 'user_devices_list'

    def get_queryset(self):
        return Device.objects.filter(user=self.request.user).values()

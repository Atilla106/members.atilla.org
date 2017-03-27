'''Views for the device model.'''
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views import generic

from ..forms.device import DeviceForm
from ..models.device import Device


class DeviceView(LoginRequiredMixin, generic.ListView):
    template_name = 'network/devices.html'
    context_object_name = 'user_devices_list'

    def get_queryset(self):
        return Device.objects.filter(user=self.request.user)


class DeviceDetailView(LoginRequiredMixin, generic.DetailView):
    model = Device

    def get_object(self, queryset=None):
        return get_object_or_404(
            Device,
            pk=self.kwargs['pk'],
            user=self.request.user,
        )


class DeviceCreateView(LoginRequiredMixin, generic.edit.CreateView):
    '''Add the current user as device owner.'''
    form_class = DeviceForm
    model = Device


class DeviceUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    success_url = reverse_lazy('network:index')
    fields = ['device_name', 'description']

    def get_object(self, queryset=None):
        return get_object_or_404(
            Device,
            pk=self.kwargs['pk'],
            user=self.request.user,
        )


class DeviceDeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    success_url = reverse_lazy('network:index')
    model = Device

    def get_object(self, queryset=None):
        return get_object_or_404(
            Device,
            pk=self.kwargs['pk'],
            user=self.request.user,
        )

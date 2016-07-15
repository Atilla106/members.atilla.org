from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.views import generic

from ..models import Device

""" Views for the device model """


class DeviceView(LoginRequiredMixin, generic.ListView):
    template_name = 'network/devices.html'
    context_object_name = 'user_devices_list'

    def get_queryset(self):
        return Device.objects.filter(user=self.request.user).values()


class DeviceDetailView(generic.DetailView):
        model = Device


class DeviceCreateView(generic.edit.CreateView):
    model = Device
    fields = ['device_name', 'description']

    """ Add the current user as device owner """
    def form_valid(self, form):
        device = form.save(commit=False)
        device.user = self.request.user
        device.full_clean()
        return super(DeviceCreateView, self).form_valid(form)


class DeviceUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    success_url = reverse_lazy('network:index')
    fields = ['device_name', 'description']

    def get_object(self, queryset=None):
        return get_object_or_404(Device,
                                 pk=self.kwargs['pk'],
                                 user=self.request.user)


class DeviceDeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    success_url = reverse_lazy('network:index')
    model = Device

    def get_object(self, queryset=None):
        return get_object_or_404(Device,
                                 pk=self.kwargs['pk'],
                                 user=self.request.user)

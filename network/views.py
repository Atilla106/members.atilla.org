from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse_lazy
from django.views import generic

from .models import Device, Interface

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
        device.full_clean();
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
    template_name = 'network/device_confirm_delete.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Device,
                pk=self.kwargs['pk'],
                user=self.request.user)

class InterfaceCreateView(generic.edit.CreateView):
    model = Interface
    fields = ['interface_type', 'description', 'mac_address']

    """ Add the device referenced in url as the interface owner """
    def form_valid(self, form):
        interface = form.save(commit=False)
        device = get_object_or_404(Device,
                pk=self.kwargs['pk'],
                user=self.request.user)
        interface.device = device
        interface.full_clean();
        return super(InterfaceCreateView, self).form_valid(form)

class InterfaceUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    success_url = reverse_lazy('network:index')
    fields = ['interface_type', 'description', 'mac_address']

    def get_object(self, queryset=None):
        device = get_object_or_404(Device,
                pk=self.kwargs['pk1'],
                user=self.request.user)
        return get_object_or_404(Interface,
                pk=self.kwargs['pk2'],
                device=device)

class InterfaceDeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    success_url = reverse_lazy('network:index')
    model = Interface
    template_name = 'network/device_confirm_delete.html'

    def get_object(self, queryset=None):
        device = get_object_or_404(Device,
                pk=self.kwargs['pk1'],
                user=self.request.user)
        return get_object_or_404(Interface,
                pk=self.kwargs['pk2'],
                device=device)



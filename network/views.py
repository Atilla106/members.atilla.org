import time

from django.contrib.auth.models import User, Permission
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse_lazy
from django.views import generic

from .settings import *
from .models import Device, Interface

""" Useful functions """
def users_with_perm(perm_name):
    return User.objects.filter(
            Q(is_superuser=True) |
            Q(user_permissions__codename=perm_name) |
            Q(groups__permissions__codename=perm_name)).distinct()

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

""" Views for the interface model """
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

""" Config rendering views """
class RenderDHCPView(generic.base.View):
    def get_interfaces(self):
        return Interface.objects.filter(
                device__user__in=users_with_perm("can_publish_device"))

    def render_file(self, request):
        interface_list = self.get_interfaces()
        template = loader.get_template('network/render_dhcp.conf')
        context = {
            'interface_list': interface_list,
            'DNS_DOMAIN': DNS_DOMAIN,
            'DNS_SERVER_1': DNS_SERVER_1,
            'DNS_SERVER_2': DNS_SERVER_2,
            'DNS_DOMAIN_SEARCH': DNS_DOMAIN_SEARCH,
        }
        output = open(DHCP_CONFIG_OUTPUT, "w")
        output.write(template.render(context, request))
        output.close()

    def get(self, request, *args, **kwargs):
        self.render_file(request)
        return HttpResponse("OK")

class RenderDNSView(generic.base.View):
    def get_devices(self):
        return Device.objects.filter(
                user__in=users_with_perm("can_publish_device"))

    def render_file(self, request):
        device_list = self.get_devices()
        template = loader.get_template('network/render_dns.conf')
        context = {
            'device_list': device_list,
            'TTL': TTL,
            'NEGATIVE_CACHE_TTL': NEGATIVE_CACHE_TTL,
            'REFRESH': REFRESH,
            'RETRY': RETRY,
            'EXPIRE': EXPIRE,
            'SERIAL': DNS_BASE_SERIAL + int(time.time() / 100),
            'DNS_DOMAIN': DNS_DOMAIN,
            'DOMAIN_MAIL_SERVER': DOMAIN_MAIL_SERVER,
            'DNS_SERVER_1': DNS_SERVER_1,
            'DNS_SERVER_2': DNS_SERVER_2,
        }
        output = open(DNS_CONFIG_OUTPUT, "w")
        output.write(template.render(context, request))
        output.close()

    def get(self, request, *args, **kwargs):
        self.render_file(request)
        return HttpResponse("OK")

class RenderReverseDNSView(generic.base.View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("OK")



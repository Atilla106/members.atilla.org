import time

from django.contrib.auth.models import User
from django.db.models import Q
from django.template import loader
from django.http import HttpResponse
from django.views import generic
from django.conf import settings

from ..models import Device, Interface


class RenderView(generic.base.View):
    """ Useful functions """
    def users_with_perm(self, perm_name):
        return User.objects.filter(
            Q(is_superuser=True) |
            Q(user_permissions__codename=perm_name) |
            Q(groups__permissions__codename=perm_name)).distinct()

    def get_interfaces(self):
        return Interface.objects.filter(
                device__user__in=self.users_with_perm("can_publish_device"))

    def get_devices(self):
        return Device.objects.filter(
                user__in=self.users_with_perm("can_publish_device"))

    """ Loads config options into a dictionnary for template context """
    def get_config_dict(self):
        return {
            'TTL': settings.TTL,
            'NEGATIVE_CACHE_TTL': settings.NEGATIVE_CACHE_TTL,
            'REFRESH': settings.REFRESH,
            'RETRY': settings.RETRY,
            'EXPIRE': settings.EXPIRE,
            'SERIAL': settings.DNS_BASE_SERIAL + int(time.time() / 100),
            'DNS_DOMAIN': settings.DNS_DOMAIN,
            'DNS_DOMAIN_SEARCH': settings.DNS_DOMAIN_SEARCH,
            'DNS_SERVER_1': settings.DNS_SERVER_1,
            'DNS_SERVER_2': settings.DNS_SERVER_2,
            'REV_DNS_ORIGIN': settings.REV_DNS_ORIGIN,
            'DOMAIN_ROOT_SERVER': settings.DOMAIN_ROOT_SERVER,
            'DOMAIN_MAIL_SERVER': settings.DOMAIN_MAIL_SERVER,
            }

    def render_file(self, request, template,
                    object_list, output_path):
        template = loader.get_template(template)

        context = self.get_config_dict()
        context['object_list'] = object_list

        output = open(output_path, "w")
        output.write(template.render(context, request))
        output.close()

""" Config rendering views """


class RenderDHCPView(RenderView):
    def get(self, request, *args, **kwargs):
        interface_list = self.get_interfaces()
        self.render_file(request,
                         'network/render_dhcp.conf',
                         interface_list,
                         settings.DHCP_CONFIG_OUTPUT)
        return HttpResponse("OK")


class RenderDNSView(RenderView):
    def get(self, request, *args, **kwargs):
        device_list = self.get_devices()
        self.render_file(request,
                         'network/render_dns.conf',
                         device_list,
                         settings.DNS_CONFIG_OUTPUT)
        return HttpResponse("OK")


class RenderReverseDNSView(RenderView):
    def get(self, request, *args, **kwargs):
        device_list = self.get_devices()
        self.render_file(request,
                         'network/render_reverse_dns.conf',
                         device_list,
                         settings.REV_DNS_CONFIG_OUTPUT)
        return HttpResponse("OK")

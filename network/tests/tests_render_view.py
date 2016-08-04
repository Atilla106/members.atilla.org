import time

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, Permission
from django.conf import settings
from django.template import loader
from django.core.urlresolvers import reverse

from ..views.render import RenderView

from ..models.device import Device
from ..models.interface import Interface, ETHERNET


class RenderViewTestCase(TestCase):
    def setUp(self):
        self.can_publish_perm = Permission.objects.get(
                codename='can_publish_device')

        self.test1 = User.objects.create_user(
                'TestUser1',
                'test1@example.com',
                'We love HDM !')

        self.test1.user_permissions.add(self.can_publish_perm)

        self.test1_device1 = Device.objects.create(
                user=self.test1,
                device_name='device_1_test_user_1',
                device_ip='127.0.0.1',
                description='Description 1')

        self.test1_device1_interface1 = Interface.objects.create(
                device=self.test1_device1,
                interface_type=ETHERNET,
                mac_address='00:00:00:00:00:00')

        self.test2 = User.objects.create_user(
                'TestUser2',
                'test2@example.com',
                'We love HDM !')

        self.test2_device1 = Device.objects.create(
                user=self.test2,
                device_name='device_1_test_user_2',
                device_ip='127.0.0.2',
                description='Description 2')

        self.test2_device1_interface1 = Interface.objects.create(
                device=self.test2_device1,
                interface_type=ETHERNET,
                mac_address='00:00:00:00:00:01')

        self.factory = RequestFactory()
        self.render_view = RenderView()

        self.device_list = self.render_view.get_devices()
        self.interface_list = self.render_view.get_interfaces()

    def render_file_test(self, object_list, template_name, file_path):
        request = self.factory.get('/')
        request.user = self.client

        template = loader.get_template(template_name)
        context = self.render_view.get_config_dict()
        context['object_list'] = object_list

        output_file = open(file_path, 'r')

        self.assertEqual(
                output_file.read(),
                template.render(context, request))

    ''' Tests for RenderView class '''

    def test_user_with_perm(self):
        self.assertTrue(
                self.test1
                in self.render_view.users_with_perm('can_publish_device'))
        self.assertFalse(
                self.test2
                in self.render_view.users_with_perm('can_publish_device'))

    ''' We may have to test with more than one device / interface in
    test_get_interfaces and test_get_devices '''

    def test_get_interfaces(self):
        self.assertEqual(
                [self.test1_device1_interface1],
                list(self.render_view.get_interfaces()))

    def test_get_devices(self):
        self.assertEqual(
                [self.test1_device1],
                list(self.render_view.get_devices()))

    def test_config_dict(self):
        config = self.render_view.get_config_dict()
        keys = ('TTL',
                'NEGATIVE_CACHE_TTL',
                'REFRESH',
                'RETRY',
                'EXPIRE',
                'SERIAL',
                'DNS_DOMAIN',
                'DNS_DOMAIN_SEARCH',
                'DNS_SERVER_1',
                'DNS_SERVER_2',
                'REV_DNS_ORIGIN',
                'DOMAIN_ROOT_SERVER',
                'DOMAIN_MAIL_SERVER')

        self.assertTrue(all(key in config for key in keys))

        self.assertEqual(
                config['TTL'],
                settings.TTL)
        self.assertEqual(
                config['NEGATIVE_CACHE_TTL'],
                settings.NEGATIVE_CACHE_TTL)
        self.assertEqual(
                config['REFRESH'],
                settings.REFRESH)
        self.assertEqual(
                config['RETRY'],
                settings.RETRY)
        self.assertEqual(
                config['EXPIRE'],
                settings.EXPIRE)
        self.assertEqual(
                config['SERIAL'],
                settings.DNS_BASE_SERIAL + int(time.time() / 100))
        self.assertEqual(
                config['DNS_DOMAIN'],
                settings.DNS_DOMAIN)
        self.assertEqual(
                config['DNS_SERVER_1'],
                settings.DNS_SERVER_1)
        self.assertEqual(
                config['DNS_SERVER_2'],
                settings.DNS_SERVER_1)
        self.assertEqual(
                config['REV_DNS_ORIGIN'],
                settings.REV_DNS_ORIGIN)
        self.assertEqual(
                config['DOMAIN_ROOT_SERVER'],
                settings.DOMAIN_ROOT_SERVER)
        self.assertEqual(
                config['DOMAIN_MAIL_SERVER'],
                settings.DOMAIN_MAIL_SERVER)

    def test_render_dhcp_view(self):
        response = self.client.get(reverse('network:render_DHCP'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'OK')

        self.render_file_test(
                self.interface_list,
                'network/render_dhcp.conf',
                settings.DHCP_CONFIG_OUTPUT)

    def test_render_dns_view(self):
        response = self.client.get(reverse('network:render_DNS'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'OK')

        self.render_file_test(
                self.device_list,
                'network/render_dns.conf',
                settings.DNS_CONFIG_OUTPUT)

    def test_render_reverse_dns_view(self):
        response = self.client.get(reverse('network:render_reverse_DNS'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'OK')

        self.render_file_test(
                self.device_list,
                'network/render_reverse_dns.conf',
                settings.REV_DNS_CONFIG_OUTPUT)

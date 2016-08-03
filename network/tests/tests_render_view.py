from django.test import TestCase
from django.contrib.auth.models import User, Permission

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
                device_name="device_1_test_user_1",
                device_ip="127.0.0.1",
                description="Description 1")

        self.test1_device1_interface1 = Interface.objects.create(
                device=self.test1_device1,
                interface_type=ETHERNET,
                mac_address="00:00:00:00:00:00")

        self.test2 = User.objects.create_user(
                'TestUser2',
                'test2@example.com',
                'We love HDM !')

        self.test2_device1 = Device.objects.create(
                user=self.test2,
                device_name="device_1_test_user_2",
                device_ip="127.0.0.2",
                description="Description 2")

        self.test2_device1_interface1 = Interface.objects.create(
                device=self.test2_device1,
                interface_type=ETHERNET,
                mac_address="00:00:00:00:00:01")

        """ Tests for RenderView class """

    def test_user_with_perm(self):
        render = RenderView()
        self.assertTrue(
                self.test1 in render.users_with_perm("can_publish_device"))
        self.assertFalse(
                self.test2 in render.users_with_perm("can_publish_device"))

    def test_get_interfaces(self):
        render = RenderView()
        self.assertEqual(
                [self.test1_device1_interface1],
                list(render.get_interfaces()))

    def test_get_devices(self):
        render = RenderView()
        self.assertEqual(
                [self.test1_device1],
                list(render.get_devices()))

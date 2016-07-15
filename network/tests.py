from django.test import TestCase
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

from .models import Device, Interface


class DeviceTestCase(TestCase):
    def setUp(self):
        self.test1 = User.objects.create_user('TestUser1', 'test1@example.com',
                                              'We love HDM !')
        self.test2 = User.objects.create_user('TestUser2', 'test2@example.com',
                                              'We love HDM !')

        self.test1_device1 = Device.objects.create(user=self.test1,
                device_name="device_1_test_user_1",
                device_ip="127.0.0.1", description="Stardard description 1")

        self.test2_device1 = Device.objects.create(user=self.test2,
                device_name="device_1_test_user_2",
                device_ip="127.0.0.2", description="Stardard description 2")

    def test_device_different_IPs(self):
        """ A device should have a unique IP address """
        with self.assertRaises(IntegrityError):
            Device.objects.create(user=self.test1,
                    device_name="device_2_test_user_1",
                    device_ip="127.0.0.1")

    def test_device_different_names(self):
        """ User devices should have differents names """
        with self.assertRaises(ValidationError):
            Device(user=self.test1, device_name="device_1_test_user_1",
                    device_ip="127.0.0.3").clean()

    def test_device_name_format(self):
        """ A device should have a alphanumeric name
        (- and _ are also accepted) """
        with self.assertRaises(ValidationError):
            Device(user=self.test1, device_name="device with spaces",
                    device_ip="127.0.0.3").full_clean()

    def test_interface_mac_format(self):
        """ An interface should have a correct MAC address """
        with self.assertRaises(ValidationError):
            Interface(device=self.test1_device1,
                    mac_address="__:__:__:__:__:__").full_clean()
        with self.assertRaises(ValidationError):
            Interface(device=self.test1_device1,
                    mac_address="ab:cd:ef:gh:12:34").full_clean()
        with self.assertRaises(ValidationError):
            Interface(device=self.test1_device1,
                    mac_address="ab:cd:ab:54:12").full_clean()

from django.test import TestCase
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.conf import settings
from django.test import Client
from django.core.urlresolvers import reverse

from ..models.device import Device


class DeviceModelTestCase(TestCase):
    def setUp(self):
        self.test1 = User.objects.create_user(
                'TestUser1',
                'test1@example.com',
                'We love HDM !')

        self.test2 = User.objects.create_user(
                'TestUser2',
                'test2@example.com',
                'We love HDM !')

        self.test1_device1 = Device.objects.create(
                user=self.test1,
                device_name="device_1_test_user_1",
                device_ip="127.0.0.1",
                description="Standard description 1")

    def test_device_different_IPs(self):
        """ A device should have a unique IP address """
        with self.assertRaises(IntegrityError):
            Device.objects.create(user=self.test1,
                                  device_name="device_2_test_user_1",
                                  device_ip="127.0.0.1")

    def test_device_different_names(self):
        """ User devices should have differents names """
        with self.assertRaises(ValidationError):
            Device(user=self.test1,
                   device_name="device_1_test_user_1",
                   device_ip="127.0.0.3").clean()

    def test_device_name_format(self):
        """ A device should have a alphanumeric name
        (- and _ are also accepted) """
        with self.assertRaises(ValidationError):
            Device(user=self.test1,
                   device_name="device with spaces",
                   device_ip="127.0.0.3").full_clean()

    def test_max_devices_per_user(self):
        for i in range(1, settings.MAX_DEVICE_PER_USER):
            tmp = Device.objects.create(user=self.test2,
                                        device_name="device" + str(i),
                                        device_ip="0.0.0." + str(i))
            tmp.save()
        with self.assertRaises(ValidationError):
            final = Device.objects.create(user=self.test2,
                                          device_name="deviceFinal",
                                          device_ip="42.42.42.42")
            final.save()


class DeviceViewTestCase(TestCase):
    def setUp(self):
        self.test1 = User.objects.create_user(
                'TestUser1',
                'test1@example.com',
                'We love HDM !')

        self.test1_device1 = Device.objects.create(
                user=self.test1,
                device_name="device_1_test_user_1",
                device_ip="127.0.0.1",
                description="Standard description 1")

        self.client = Client()
        self.client.login(username='TestUser1', password='We love HDM !')

    def tearDown(self):
        self.test1.delete()

    def test_view_get_queryset(self):
        """ get_queryset should return an array of Devices """
        response = self.client.get(reverse('network:index'))
        device_list = response.context['user_devices_list']
        self.assertTrue([all(isinstance(x, Device) for x in device_list)])
        self.assertTrue(device_list.count != 0)

from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from django.core.urlresolvers import reverse

from ..models.device import Device


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

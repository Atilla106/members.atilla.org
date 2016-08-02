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

        self.test2 = User.objects.create_user(
                'TestUser2',
                'test2@example.com',
                'We love HDM !')

        self.test1_device1 = Device.objects.create(
                user=self.test1,
                device_name="device_1_test_user_1",
                device_ip="127.0.0.1",
                description="Standard description 1")

        self.test2_device1 = Device.objects.create(
                user=self.test2,
                device_name="device_1_test_user_2",
                device_ip="127.0.0.2",
                description="Standard description 2")

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

    def test_create_view_form_valid(self):
        pass

    def test_update_view_get_object(self):
        """ The view should return a Device owned by the current user or
        throw a 404 error """

        """ Try with a device owned by the user """
        response1 = self.client.get(reverse(
            'network:device_update',
            args=[self.test1_device1.pk]))
        self.assertTrue(self.test1_device1 == response1.context['device'])

        """ Try with a device owned by another user """
        response2 = self.client.get(reverse(
            'network:device_update',
            args=[self.test2_device1.pk]))
        self.assertTrue(response2.status_code == 404)

        """ Try with a device that does not exists """
        response2 = self.client.get(reverse(
            'network:device_update',
            args=[42133742]))
        self.assertTrue(response2.status_code == 404)

    def test_delete_view_get_object(self):
        """ The view should return a Device owned by the current user or
        throw a 404 error """

        """ Try with a device owned by the user """
        response1 = self.client.get(reverse(
            'network:device_delete',
            args=[self.test1_device1.pk]))
        self.assertTrue(self.test1_device1 == response1.context['device'])

        """ Try with a device owned by another user """
        response2 = self.client.get(reverse(
            'network:device_delete',
            args=[self.test2_device1.pk]))
        self.assertTrue(response2.status_code == 404)

        """ Try with a device that does not exists """
        response2 = self.client.get(reverse(
            'network:device_delete',
            args=[42133742]))
        self.assertTrue(response2.status_code == 404)

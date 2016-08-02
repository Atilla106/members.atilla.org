from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from django.core.urlresolvers import reverse
from django.conf import settings

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

        self.anonymous = Client()

        self.client.login(username='TestUser1', password='We love HDM !')

    def tearDown(self):
        self.test1.delete()

    """ Generic test methods """

    def deny_anonymous_test(self, view_name, args=[]):
        response = self.anonymous.get(
                reverse(view_name, args=args),
                follow=True)
        self.assertRedirects(
                response,
                (settings.LOGIN_URL + "?next=" + reverse(view_name,
                                                         args=args)))

    def load_test(self, view_name, template_name, args=[]):
        response = self.client.get(
                reverse(view_name, args=args),
                follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name)

    def get_object_test(self, view_name):
        """ The view should return a Device owned by the current user or
        throw a 404 error """

        """ Try with a device owned by the user """
        response1 = self.client.get(reverse(
                view_name,
                args=[self.test1_device1.pk]))
        self.assertEqual(self.test1_device1, response1.context['device'])

        """ Try with a device owned by another user """
        response2 = self.client.get(reverse(
                view_name,
                args=[self.test2_device1.pk]))
        self.assertEqual(response2.status_code, 404)

        """ Try with a device that does not exists """
        response3 = self.client.get(reverse(
                view_name,
                args=[42133742]))
        self.assertEqual(response3.status_code, 404)

    """ Tests for DeviceView class """

    def test_view_deny_anonymous(self):
        self.deny_anonymous_test('network:index')

    def test_view_loads(self):
        self.load_test('network:index', 'network/devices.html')

    def test_view_get_queryset(self):
        """ get_queryset should return an array of Devices """
        response = self.client.get(reverse('network:index'))
        device_list = response.context['user_devices_list']
        self.assertTrue(all([isinstance(x, Device) for x in device_list]))
        self.assertNotEqual(device_list.count, 0)

    """ Tests for DeviceDetailView class """

    def test_detail_view_deny_anonymous(self):
        self.deny_anonymous_test(
                'network:device_detail',
                args=[self.test1_device1.pk])

    def test_detail_view_loads(self):
        self.load_test(
                'network:device_detail',
                'network/device_detail.html',
                args=[self.test1_device1.pk])

    def test_detail_view_get_object(self):
        self.get_object_test('network:device_detail')

    """ Tests for DeviceCreateView class """

    def test_create_view_deny_anonymous(self):
        self.deny_anonymous_test('network:device_create')

    def test_create_view_loads(self):
        self.load_test(
                'network:device_create',
                'network/device_form.html')

    def test_create_view_form_valid(self):
        """ The registered device should have a unique name and should belong
        to the current user.
        The name should also match the database requirements """

        """ Try with a correct device """
        self.client.post(
                reverse('network:device_create'),
                {'device_name': 'NewDevice1', 'description': 'New device 1'})
        newDevice = Device.objects.filter(
                user=self.test1,
                device_name='NewDevice1')
        self.assertNotEqual(newDevice, [])

        """ Try with an incorrect device name """
        response2 = self.client.post(
                reverse('network:device_create'),
                {'device_name': 'New Device 2', 'description': 'New device 2'})
        self.assertContains(
                response2,
                "Invalid name",
                html=False)

        """ Try with a device name aleready taken """
        response3 = self.client.post(
                reverse('network:device_create'),
                {'device_name': 'device_1_test_user_1',
                    'description': 'New device 3'})
        self.assertContains(
                response3,
                "Device name aleready taken",
                html=False)

    """ Tests for DeviceUpdateView class """

    def test_update_view_deny_anonymous(self):
        self.deny_anonymous_test(
                'network:device_update',
                args=[self.test1_device1.pk])

    def test_update_view_loads(self):
        self.load_test(
                'network:device_update',
                'network/device_form.html',
                args=[self.test1_device1.pk])

    def test_update_view_get_object(self):
        self.get_object_test('network:device_update')

    def test_update_view_commit(self):
        """ A device should only be editable by the device owner
        The primary key given in request should match a device in db """

        """ Try with a device owned by the user """
        response1 = self.client.post(
                reverse('network:device_update',
                        args=[self.test1_device1.pk]),
                {'device_name': 'device_1_test_user_1', 'description': '4242'})
        self.assertEqual(response1.status_code, 302)
        self.assertRedirects(response1, reverse('network:index'))

    """ Test for DeviceDeleteView class """

    def test_delete_view_deny_anonymous(self):
        self.deny_anonymous_test(
                'network:device_delete',
                args=[self.test1_device1.pk])

    def test_delete_view_loads(self):
        self.load_test(
                'network:device_delete',
                'network/device_confirm_delete.html',
                args=[self.test1_device1.pk])

    def test_delete_view_get_object(self):
        self.get_object_test('network:device_delete')

    def test_delete_view_commit(self):
        """ A device should only be deleted by the device owner
        The primary key given in request should match a device in db """

        """ Try with a device owned by the user """
        response1 = self.client.post(
                reverse('network:device_delete',
                        args=[self.test1_device1.pk]))
        self.assertEqual(response1.status_code, 302)
        self.assertRedirects(response1, reverse('network:index'))

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

from ..models.device import Device


class DeviceModelTestCase(TestCase):
    def setUp(self):
        self.test1 = User.objects.create_user(
            username='TestUser1',
            email='test1@example.com',
            password='We love HDM !',
        )

        self.test2 = User.objects.create_user(
            username='TestUser2',
            email='test2@example.com',
            password='We love HDM !',
        )

        self.test1_device1 = Device.objects.create(
            user=self.test1,
            device_name='device-1-test-user-1',
            device_ip='127.0.0.1',
            description='Standard description 1',
        )

    def test_device_different_IPs(self):
        '''A device should have a unique IP address.'''
        with self.assertRaises(IntegrityError):
            Device.objects.create(
                user=self.test1,
                device_name='device-2-test-user-1',
                device_ip='127.0.0.1',
            )

    def test_device_different_names(self):
        '''User devices should have differents names.'''
        with self.assertRaises(ValidationError):
            Device(
                user=self.test1,
                device_name='device-1-test-user-1',
                device_ip='127.0.0.3',
            ).clean()

    def test_device_name_format(self):
        '''A device should have a alphanumeric name
        (- and _ are also accepted).'''
        with self.assertRaises(ValidationError):
            Device(
                user=self.test1,
                device_name='device with spaces',
                device_ip='127.0.0.3',
            ).full_clean()

        ''' Check that a device containing special chars can be created '''
        self.assertEqual(
            type(Device.objects.create(
                user=self.test1,
                device_name='device-with-special-chars',
                device_ip='10.42.42.1')),
            Device)

    def test_max_devices_per_user(self):
        for i in range(1, settings.MAX_DEVICE_PER_USER):
            tmp = Device.objects.create(
                user=self.test2,
                device_name='device' + str(i),
                device_ip='0.0.0.' + str(i),
            )
            tmp.save()

        with self.assertRaises(ValidationError):
            final = Device.objects.create(
                user=self.test2,
                device_name='deviceFinal',
                device_ip='42.42.42.42',
            )
            final.save()

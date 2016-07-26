from django.test import TestCase
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.conf import settings

from ..models.device import Device
from ..models.interface import Interface


class InterfaceTestCase(TestCase):
    def setUp(self):
        self.test1 = User.objects.create_user('TestUser1', 'test1@example.com',
                                              'We love HDM !')

        self.test1_device1 = Device.objects.create(user=self.test1,
                                                   device_name="device_1_test"
                                                               "_user_1",
                                                   device_ip="127.0.0.1",
                                                   description="Standard"
                                                               " description 1"
                                                   )

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

    def test_max_interfaces_per_device(self):
        for i in range(1, settings.MAX_INTERFACE_PER_DEVICE):
            tmp = Interface.objects.create(device=self.test1_device1,
                                           mac_address=("ab:cd:ef:ab:12:3"
                                                        + str(i)))
            tmp.save()
        with self.assertRaises(ValidationError):
            final = Interface.objects.create(device=self.test1_device1,
                                             mac_address="ab:cd:ef:ab:13:FF")
            final.save()

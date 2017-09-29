from captcha.conf import settings

from django.test import TestCase
from django.core.urlresolvers import reverse

from ..models import PendingUser


class RegisterViewTestCase(TestCase):
    def test_view_loads(self):
        response = self.client.get(reverse('accounts:register'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_register_view_form_valid(self):
        ''' The first and last name should be defined.
        The given email address should be a valid email. '''

        settings.CAPTCHA_TEST_MODE = True

        # Try with correct informations
        self.client.post(
            reverse('accounts:register'),
            {'first_name': 'Potato',
                'last_name': 'Chips',
                'email': 'potato.chips@lustucru.org',
                'captcha_0': 'hash',
                'captcha_1': 'passed',
                'agreement': 'true'},
        )

        newUser = PendingUser.objects.filter(first_name='Potato')
        self.assertNotEqual(list(newUser), [])

        # Try with an incorrect email
        self.client.post(
            reverse('accounts:register'),
            {'first_name': 'Mister',
                'last_name': 'Tomaato',
                'email': 'randomfalseemail',
                'captcha_0': 'hash',
                'captcha_1': 'passed',
                'agreement': 'true'},
        )

        newUser2 = PendingUser.objects.filter(first_name='Mister')
        self.assertEqual(list(newUser2), [])

        # Try with no 'agreement' boolean
        self.client.post(
            reverse('accounts:register'),
            {'first_name': 'Little',
                'last_name': 'Cupcake',
                'email': 'little.cupcake@haribo.org',
                'captcha_0': 'hash',
                'captcha_1': 'passed'}
        )

        newUser3 = PendingUser.objects.filter(first_name='Little')
        self.assertEqual(list(newUser3), [])

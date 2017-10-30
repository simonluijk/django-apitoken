from datetime import datetime
from mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model
from .api import TokenAPI


class APITestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create()
        self.api = TokenAPI()

    def test_attributes(self):
        self.assertEqual(TokenAPI.STANDARD, 'standard')
        self.assertEqual(TokenAPI.APP, 'app')
        self.assertEqual(TokenAPI.OTP_TMP, 'otp-tmp')
        self.assertEqual(TokenAPI.OTP_VERIFIED, 'otp-verified')

    @patch('apitoken.api.now')
    def test_create(self, mnow):
        mnow.return_value = datetime(2011, 6, 21, 9, 43, 33)
        token = self.api.create(self.user, typ=TokenAPI.STANDARD)
        self.assertEqual(token.user, self.user)
        self.assertEqual(token.typ, 'standard')
        self.assertEqual(token.life, 60 * 60 * 4)
        self.assertEqual(token.expires, datetime(2011, 6, 21, 13, 43, 33))

    @patch('apitoken.api.now')
    def test_get(self, mnow):
        # Create initial token
        mnow.return_value = datetime(2011, 6, 21, 9, 43, 33)
        token = self.api.create(self.user, typ=TokenAPI.STANDARD)

        # Validate when still valid
        mnow.return_value = datetime(2011, 6, 21, 10, 43, 33)
        token = self.api.get(token.token)
        self.assertEqual(token.user, self.user)
        self.assertEqual(token.typ, 'standard')
        self.assertEqual(token.life, 60 * 60 * 4)
        self.assertEqual(token.expires, datetime(2011, 6, 21, 14, 43, 33))

        # Validate expired
        mnow.return_value = datetime(2011, 6, 21, 14, 43, 34)
        token = self.api.get(token.token)
        self.assertIsNone(token)

    def test_delete(self):
        token = self.api.create(self.user, typ=TokenAPI.STANDARD)
        token.delete()
        token = self.api.get(token.token)
        self.assertIsNone(token)

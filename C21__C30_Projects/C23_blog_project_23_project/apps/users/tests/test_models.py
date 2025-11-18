from django.test import TestCase
from django.contrib.auth.models import User
from ninja.testing import TestClient
from ..api import router
from ..models import UserToken, UserProfile


class UserTokenModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

    def test_token_generation(self):
        token = UserToken.generate_token()

        self.assertIsNotNone(token)
        self.assertLessEqual(len(token), 256)

    def test_create_for_user(self):
        user_token = UserToken.create_for_user(self.user)

        self.assertEqual(user_token.user, self.user)
        self.assertTrue(user_token.is_active)
        self.assertLessEqual(len(user_token.token), 256)
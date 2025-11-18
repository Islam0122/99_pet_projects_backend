from django.test import TestCase
from django.contrib.auth.models import User
from ninja.testing import TestClient
from ..api import router
from ..models import UserToken, UserProfile


class UserLoginTest(TestCase):
    def setUp(self):
        self.client = TestClient(router)
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        UserProfile.objects.create(user=self.user)

    def test_login_success(self):
        response = self.client.post("/login", json={
            "username": "testuser",
            "password": "testpass123"
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.json())
        self.assertIn("refresh", response.json())

    def test_login_invalid_credentials(self):
        response = self.client.post("/login", json={
            "username": "testuser",
            "password": "wrongpassword"
        })

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["detail"], "Invalid credentials")

    def test_login_custom_token(self):
        response = self.client.post("/login-custom", json={
            "username": "testuser",
            "password": "testpass123"
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json())
        token_count = UserToken.objects.filter(user=self.user, is_active=True).count()
        self.assertEqual(token_count, 1)

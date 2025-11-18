from django.test import TestCase
from django.contrib.auth.models import User
from ninja.testing import TestClient
from ..api import router


class UserRegistrationTest(TestCase):
    def setUp(self):
        self.client = TestClient(router)

    def test_register_success(self):
        response = self.client.post("/register", json={
            "username": "testuser",
            "password": "testpass123"
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.json())
        self.assertIn("refresh", response.json())
        user = User.objects.get(username="testuser")
        self.assertIsNotNone(user)
        self.assertTrue(hasattr(user, 'profile'))

    def test_register_duplicate_username(self):
        User.objects.create_user(username="testuser", password="testpass123")

        response = self.client.post("/register", json={
            "username": "testuser",
            "password": "anotherpass"
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Username already exists")

    def test_register_custom_token(self):
        response = self.client.post("/register-custom", json={
            "username": "customuser",
            "password": "testpass123"
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json())
        self.assertIn("user", response.json())
        token = response.json()["token"]
        self.assertLessEqual(len(token), 256)
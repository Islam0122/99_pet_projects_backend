from django.test import TestCase
from django.contrib.auth.models import User
from ninja.testing import TestClient
from ..api import router
from ..models import UserToken, UserProfile


class CustomTokenTest(TestCase):
    def setUp(self):
        self.client = TestClient(router)
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        UserProfile.objects.create(user=self.user)

    def test_custom_token_authentication(self):
        login_response = self.client.post("/login-custom", json={
            "username": "testuser",
            "password": "testpass123"
        })

        custom_token = login_response.json()["token"]
        profile_response = self.client.get(
            "/profile-custom",
            headers={"Authorization": f"Bearer {custom_token}"}
        )

        self.assertEqual(profile_response.status_code, 200)
        self.assertEqual(profile_response.json()["username"], "testuser")

    def test_custom_token_logout(self):
        login_response = self.client.post("/login-custom", json={
            "username": "testuser",
            "password": "testpass123"
        })

        custom_token = login_response.json()["token"]

        logout_response = self.client.post(
            "/logout-custom",
            headers={"Authorization": f"Bearer {custom_token}"}
        )

        self.assertEqual(logout_response.status_code, 200)

        token = UserToken.objects.get(token=custom_token)
        self.assertFalse(token.is_active)

        profile_response = self.client.get(
            "/profile-custom",
            headers={"Authorization": f"Bearer {custom_token}"}
        )

        self.assertEqual(profile_response.status_code, 401)

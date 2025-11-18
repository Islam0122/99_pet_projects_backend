from django.test import TestCase
from django.contrib.auth.models import User
from ninja.testing import TestClient
from ..api import router
from ..models import UserToken, UserProfile


class UserProfileTest(TestCase):
    def setUp(self):
        self.client = TestClient(router)
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            email="test@example.com"
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            bio="Test bio"
        )
        response = self.client.post("/login", json={
            "username": "testuser",
            "password": "testpass123"
        })
        self.access_token = response.json()["access"]

    def test_get_profile_success(self):
        response = self.client.get(
            "/profile",
            headers={"Authorization": f"Bearer {self.access_token}"}
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["username"], "testuser")
        self.assertEqual(data["email"], "test@example.com")
        self.assertEqual(data["profile"]["bio"], "Test bio")

    def test_get_profile_unauthorized(self):
        response = self.client.get("/profile")

        self.assertEqual(response.status_code, 401)

    def test_update_profile_success(self):
        response = self.client.put(
            "/profile",
            json={
                "bio": "Updated bio",
                "avatar": "https://example.com/avatar.jpg"
            },
            headers={"Authorization": f"Bearer {self.access_token}"}
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["profile"]["bio"], "Updated bio")
        self.assertEqual(data["profile"]["avatar"], "https://example.com/avatar.jpg")

        self.profile.refresh_from_db()
        self.assertEqual(self.profile.bio, "Updated bio")

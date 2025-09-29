from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from apps.user.models import User

class UserAuthTests(APITestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.protected_url = reverse('protected')
        self.logout_url = reverse('logout')
        self.user_data = {
            "username": "islam",
            "email": "islam@example.com",
            "first_name": "Islam",
            "last_name": "Dev",
            "password": "strongpassword123",
            "password2": "strongpassword123"
        }

    def test_user_registration(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, "islam@example.com")

    def test_user_login_and_access_protected(self):
        self.client.post(self.register_url, self.user_data, format='json')

        login_data = {"email": "islam@example.com", "password": "strongpassword123"}
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

        access_token = response.data['access']
        refresh_token = response.data['refresh']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Welcome", response.data['message'])

        response = self.client.post(self.logout_url, {"refresh": refresh_token}, format='json')
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

        response = self.client.post(reverse('token_refresh'), {"refresh": refresh_token}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.users.models import User, Role, UserRole
from django.utils import timezone
from datetime import timedelta


@pytest.mark.django_db
class TestUserRegistration:

    def setup_method(self):
        self.client = APIClient()
        self.register_url = reverse('register')

    def test_successful_registration(self):
        data = {
            'email': 'newuser@example.com',
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'password': 'securepass123',
            'password2': 'securepass123'
        }

        response = self.client.post(self.register_url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert 'user' in response.data
        assert response.data['user']['email'] == 'newuser@example.com'
        assert response.data['user']['is_verified'] is False

        user = User.objects.get(email='newuser@example.com')
        assert user.first_name == 'Иван'
        assert user.check_password('securepass123')
        assert user.otp_code is not None

    def test_registration_password_mismatch(self):
        data = {
            'email': 'test@example.com',
            'first_name': 'Тест',
            'last_name': 'Тестов',
            'password': 'password123',
            'password2': 'different123'
        }

        response = self.client.post(self.register_url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'password' in response.data or 'non_field_errors' in response.data

    def test_registration_duplicate_email(self):
        User.objects.create_user(
            email='existing@example.com',
            first_name='Существующий',
            last_name='Пользователь',
            password='pass123'
        )

        data = {
            'email': 'existing@example.com',
            'first_name': 'Новый',
            'last_name': 'Пользователь',
            'password': 'newpass123',
            'password2': 'newpass123'
        }

        response = self.client.post(self.register_url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data

    def test_registration_short_password(self):
        data = {
            'email': 'test@example.com',
            'first_name': 'Тест',
            'last_name': 'Тестов',
            'password': '123',
            'password2': '123'
        }

        response = self.client.post(self.register_url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUserLogin:
    def setup_method(self):
        self.client = APIClient()
        self.login_url = reverse('login')
        self.user = User.objects.create_user(
            email='verified@example.com',
            first_name='Верифицированный',
            last_name='Пользователь',
            password='testpass123'
        )
        self.user.is_verified = True
        self.user.save()

    def test_successful_login(self):
        data = {
            'email': 'verified@example.com',
            'password': 'testpass123'
        }

        response = self.client.post(self.login_url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert 'token' in response.data
        assert response.data['message'] == 'Успешный вход'

    def test_login_wrong_password(self):
        data = {
            'email': 'verified@example.com',
            'password': 'wrongpassword'
        }

        response = self.client.post(self.login_url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_nonexistent_user(self):
        data = {
            'email': 'nonexistent@example.com',
            'password': 'somepass123'
        }

        response = self.client.post(self.login_url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_unverified_user(self):
        unverified_user = User.objects.create_user(
            email='unverified@example.com',
            first_name='Не',
            last_name='Верифицирован',
            password='pass123'
        )

        data = {
            'email': 'unverified@example.com',
            'password': 'pass123'
        }

        response = self.client.post(self.login_url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'не подтверждён' in str(response.data).lower()

    def test_login_inactive_user(self):
        inactive_user = User.objects.create_user(
            email='inactive@example.com',
            first_name='Неактивный',
            last_name='Пользователь',
            password='pass123'
        )
        inactive_user.is_verified = True
        inactive_user.is_active = False
        inactive_user.save()

        data = {
            'email': 'inactive@example.com',
            'password': 'pass123'
        }

        response = self.client.post(self.login_url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestOTPVerification:

    def setup_method(self):
        self.client = APIClient()
        self.verify_url = reverse('verify-otp')

        self.user = User.objects.create_user(
            email='test@example.com',
            first_name='Тест',
            last_name='Тестов',
            password='pass123'
        )
        self.user.otp_code = '123456'
        self.user.otp_expires_at = timezone.now() + timedelta(minutes=10)
        self.user.save()

    def test_successful_otp_verification(self):
        data = {
            'email': 'test@example.com',
            'otp_code': '123456'
        }

        response = self.client.post(self.verify_url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert 'успешно подтверждён' in response.data['message'].lower()

        self.user.refresh_from_db()
        assert self.user.is_verified is True
        assert self.user.otp_code is None

    def test_wrong_otp_code(self):
        data = {
            'email': 'test@example.com',
            'otp_code': '999999'
        }

        response = self.client.post(self.verify_url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'неверный' in str(response.data).lower()

    def test_expired_otp(self):
        self.user.otp_expires_at = timezone.now() - timedelta(minutes=1)
        self.user.save()

        data = {
            'email': 'test@example.com',
            'otp_code': '123456'
        }

        response = self.client.post(self.verify_url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'истёк' in str(response.data).lower()


@pytest.mark.django_db
class TestProfileManagement:
    def setup_method(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            email='user@example.com',
            first_name='Пользователь',
            last_name='Тестовый',
            password='pass123'
        )
        self.user.is_verified = True
        self.user.save()

        login_response = self.client.post(
            reverse('login'),
            {'email': 'user@example.com', 'password': 'pass123'},
            format='json'
        )
        self.token = login_response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_get_profile(self):
        response = self.client.get(reverse('profile'))
        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == 'user@example.com'
        assert response.data['first_name'] == 'Пользователь'

    def test_get_profile_unauthorized(self):
        self.client.credentials()
        response = self.client.get(reverse('profile'))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED  # ✅ Изменено
    def test_update_profile(self):
        data = {
            'first_name': 'Обновлённое',
            'last_name': 'Имя'
        }

        response = self.client.patch(
            reverse('profile-update'),
            data,
            format='json'
        )
        assert response.status_code == status.HTTP_200_OK
        self.user.refresh_from_db()
        assert self.user.first_name == 'Обновлённое'
        assert self.user.last_name == 'Имя'


@pytest.mark.django_db
class TestJWTAuthentication:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='jwt@example.com',
            first_name='JWT',
            last_name='User',
            password='pass123'
        )
        self.user.is_verified = True
        self.user.save()
        login_response = self.client.post(
            reverse('login'),
            {'email': 'jwt@example.com', 'password': 'pass123'},
            format='json'
        )
        self.token = login_response.data['token']

    def test_access_with_valid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(reverse('protected'))
        assert response.status_code == status.HTTP_200_OK
        assert 'Добро пожаловать' in response.data['message']

    def test_access_without_token(self):
        response = self.client.get(reverse('protected'))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED  # ✅ Изменено

    def test_access_with_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid_token_here')
        response = self.client.get(reverse('protected'))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED  # ✅ Изменено

    def test_logout(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.post(reverse('logout'))
        assert response.status_code == status.HTTP_200_OK
        assert 'выход' in response.data['message'].lower()
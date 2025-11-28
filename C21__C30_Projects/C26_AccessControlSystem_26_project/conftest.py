import pytest
from django.core.management import call_command


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'fixtures/initial_data.json')


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def authenticated_client(db, api_client):
    from apps.users.models import User
    from django.urls import reverse

    def _create_client(email='test@example.com', password='testpass123', is_verified=True):
        user = User.objects.create_user(
            email=email,
            first_name='Test',
            last_name='User',
            password=password
        )
        user.is_verified = is_verified
        user.save()

        response = api_client.post(
            reverse('login'),
            {'email': email, 'password': password},
            format='json'
        )

        if response.status_code == 200:
            token = response.data['token']
            api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        return api_client, user

    return _create_client


@pytest.fixture
def sample_user(db):
    from apps.users.models import User

    user = User.objects.create_user(
        email='sample@example.com',
        first_name='Sample',
        last_name='User',
        password='samplepass123'
    )
    user.is_verified = True
    user.save()
    return user


@pytest.fixture
def sample_role(db):
    from apps.users.models import Role

    return Role.objects.create(
        name='test_role',
        description='Test role for testing'
    )


@pytest.fixture
def sample_business_element(db):
    from apps.access.models import BusinessElement

    return BusinessElement.objects.create(
        name='test_element',
        description='Test business element'
    )


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def mock_email_backend(settings):
    settings.EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
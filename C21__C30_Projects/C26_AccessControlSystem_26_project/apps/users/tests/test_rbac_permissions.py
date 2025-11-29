import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.users.models import User, Role, UserRole
from apps.access.models import BusinessElement, AccessRolesRules


@pytest.fixture
def setup_roles_and_elements(db):

    admin_role, _ = Role.objects.get_or_create(
        name='admin',
        defaults={'description': 'Администратор'}
    )
    manager_role, _ = Role.objects.get_or_create(
        name='manager',
        defaults={'description': 'Менеджер'}
    )
    user_role, _ = Role.objects.get_or_create(
        name='user',
        defaults={'description': 'Пользователь'}
    )
    guest_role, _ = Role.objects.get_or_create(
        name='guest',
        defaults={'description': 'Гость'}
    )

    products, _ = BusinessElement.objects.get_or_create(
        name='products',
        defaults={'description': 'Товары'}
    )
    orders, _ = BusinessElement.objects.get_or_create(
        name='orders',
        defaults={'description': 'Заказы'}
    )
    stores, _ = BusinessElement.objects.get_or_create(
        name='stores',
        defaults={'description': 'Магазины'}
    )

    AccessRolesRules.objects.get_or_create(
        role=admin_role,
        element=products,
        defaults={
            'read_permission': True,
            'read_all_permission': True,
            'create_permission': True,
            'update_permission': True,
            'update_all_permission': True,
            'delete_permission': True,
            'delete_all_permission': True
        }
    )

    AccessRolesRules.objects.get_or_create(
        role=admin_role,
        element=orders,
        defaults={
            'read_permission': True,
            'read_all_permission': True,
            'create_permission': True,
            'update_permission': True,
            'update_all_permission': True,
            'delete_permission': True,
            'delete_all_permission': True
        }
    )

    AccessRolesRules.objects.get_or_create(
        role=manager_role,
        element=products,
        defaults={
            'read_permission': True,
            'read_all_permission': True,
            'create_permission': True,
            'update_permission': True,
            'update_all_permission': True,
            'delete_permission': True,
            'delete_all_permission': False
        }
    )

    AccessRolesRules.objects.get_or_create(
        role=manager_role,
        element=orders,
        defaults={
            'read_permission': True,
            'read_all_permission': True,
            'create_permission': False,
            'update_permission': True,
            'update_all_permission': True,
            'delete_permission': False,
            'delete_all_permission': False
        }
    )

    AccessRolesRules.objects.get_or_create(
        role=user_role,
        element=products,
        defaults={
            'read_permission': True,
            'read_all_permission': True,
            'create_permission': False,
            'update_permission': False,
            'update_all_permission': False,
            'delete_permission': False,
            'delete_all_permission': False
        }
    )

    AccessRolesRules.objects.get_or_create(
        role=user_role,
        element=orders,
        defaults={
            'read_permission': True,
            'read_all_permission': False,
            'create_permission': True,
            'update_permission': True,
            'update_all_permission': False,
            'delete_permission': True,
            'delete_all_permission': False
        }
    )

    AccessRolesRules.objects.get_or_create(
        role=guest_role,
        element=products,
        defaults={
            'read_permission': True,
            'read_all_permission': True,
            'create_permission': False,
            'update_permission': False,
            'update_all_permission': False,
            'delete_permission': False,
            'delete_all_permission': False
        }
    )

    return {
        'roles': {
            'admin': admin_role,
            'manager': manager_role,
            'user': user_role,
            'guest': guest_role
        },
        'elements': {
            'products': products,
            'orders': orders,
            'stores': stores
        }
    }


@pytest.fixture
def create_user_with_role(db):
    def _create(email, role_name, role_obj):
        user = User.objects.create_user(
            email=email,
            first_name='Test',
            last_name='User',
            password='testpass123'
        )
        user.is_verified = True
        user.save()

        UserRole.objects.create(user=user, role=role_obj)
        return user

    return _create


@pytest.fixture
def get_auth_client():
    def _get_client(user):
        client = APIClient()
        login_response = client.post(
            reverse('login'),
            {'email': user.email, 'password': 'testpass123'},
            format='json'
        )
        token = login_response.data['token']
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        return client

    return _get_client


@pytest.mark.django_db
class TestAdminPermissions:
    def test_admin_can_read_all_products(self, setup_roles_and_elements, create_user_with_role, get_auth_client):
        admin = create_user_with_role(
            'admin@test.com',
            'admin',
            setup_roles_and_elements['roles']['admin']
        )
        client = get_auth_client(admin)

        response = client.get(reverse('products-list-create'))

        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert response.data['count'] >= 4

    def test_admin_can_create_product(self, setup_roles_and_elements, create_user_with_role, get_auth_client):
        admin = create_user_with_role(
            'admin@test.com',
            'admin',
            setup_roles_and_elements['roles']['admin']
        )
        client = get_auth_client(admin)

        data = {'name': 'Новый товар', 'price': 10000}
        response = client.post(reverse('products-list-create'), data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['product']['name'] == 'Новый товар'

    def test_admin_can_update_any_product(self, setup_roles_and_elements, create_user_with_role, get_auth_client):
        admin = create_user_with_role(
            'admin@test.com',
            'admin',
            setup_roles_and_elements['roles']['admin']
        )
        client = get_auth_client(admin)

        data = {'name': 'Обновлённый товар', 'price': 55000}
        response = client.put(reverse('products-detail', kwargs={'pk': 1}), data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert 'обновлён' in response.data['message'].lower()

    def test_admin_can_delete_any_product(self, setup_roles_and_elements, create_user_with_role, get_auth_client):
        admin = create_user_with_role(
            'admin@test.com',
            'admin',
            setup_roles_and_elements['roles']['admin']
        )
        client = get_auth_client(admin)

        response = client.delete(reverse('products-detail', kwargs={'pk': 1}))

        assert response.status_code == status.HTTP_200_OK
        assert 'удалён' in response.data['message'].lower()


@pytest.mark.django_db
class TestManagerPermissions:
    def test_manager_can_read_all_products(self, setup_roles_and_elements, create_user_with_role, get_auth_client):
        manager = create_user_with_role(
            'manager@test.com',
            'manager',
            setup_roles_and_elements['roles']['manager']
        )
        client = get_auth_client(manager)

        response = client.get(reverse('products-list-create'))

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] >= 4

    def test_manager_can_create_product(self, setup_roles_and_elements, create_user_with_role, get_auth_client):
        manager = create_user_with_role(
            'manager@test.com',
            'manager',
            setup_roles_and_elements['roles']['manager']
        )
        client = get_auth_client(manager)

        data = {'name': 'Товар от менеджера', 'price': 20000}
        response = client.post(reverse('products-list-create'), data, format='json')

        assert response.status_code == status.HTTP_201_CREATED

    def test_manager_can_update_all_products(self, setup_roles_and_elements, create_user_with_role, get_auth_client):
        manager = create_user_with_role(
            'manager@test.com',
            'manager',
            setup_roles_and_elements['roles']['manager']
        )
        client = get_auth_client(manager)

        data = {'name': 'Обновлено менеджером', 'price': 35000}
        response = client.put(reverse('products-detail', kwargs={'pk': 2}), data, format='json')

        assert response.status_code == status.HTTP_200_OK

    def test_manager_cannot_delete_products_not_owned(self, setup_roles_and_elements, create_user_with_role,
                                                      get_auth_client):
        manager = create_user_with_role(
            'manager@test.com',
            'manager',
            setup_roles_and_elements['roles']['manager']
        )
        client = get_auth_client(manager)

        response = client.delete(reverse('products-detail', kwargs={'pk': 1}))
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND]

    def test_manager_can_read_all_orders(self, setup_roles_and_elements, create_user_with_role, get_auth_client):
        manager = create_user_with_role(
            'manager@test.com',
            'manager',
            setup_roles_and_elements['roles']['manager']
        )
        client = get_auth_client(manager)

        response = client.get(reverse('orders-list-create'))

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] >= 3

    def test_manager_cannot_create_order(self, setup_roles_and_elements, create_user_with_role, get_auth_client):
        manager = create_user_with_role(
            'manager@test.com',
            'manager',
            setup_roles_and_elements['roles']['manager']
        )
        client = get_auth_client(manager)

        data = {'product_id': 1, 'quantity': 2, 'total': 100000}
        response = client.post(reverse('orders-list-create'), data, format='json')

        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestUserPermissions:

    def test_user_can_read_all_products(self, setup_roles_and_elements, create_user_with_role, get_auth_client):
        user = create_user_with_role(
            'user@test.com',
            'user',
            setup_roles_and_elements['roles']['user']
        )
        client = get_auth_client(user)

        response = client.get(reverse('products-list-create'))

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] >= 4

    def test_user_cannot_create_product(self, setup_roles_and_elements, create_user_with_role, get_auth_client):
        user = create_user_with_role(
            'user@test.com',
            'user',
            setup_roles_and_elements['roles']['user']
        )
        client = get_auth_client(user)

        data = {'name': 'Попытка создать', 'price': 5000}
        response = client.post(reverse('products-list-create'), data, format='json')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_user_cannot_update_product(self, setup_roles_and_elements, create_user_with_role, get_auth_client):
        user = create_user_with_role(
            'user@test.com',
            'user',
            setup_roles_and_elements['roles']['user']
        )
        client = get_auth_client(user)

        data = {'name': 'Попытка обновить', 'price': 6000}
        response = client.put(reverse('products-detail', kwargs={'pk': 1}), data, format='json')

        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND]

    def test_user_can_read_only_own_orders(self, setup_roles_and_elements, create_user_with_role, get_auth_client):
        user = create_user_with_role(
            'user@test.com',
            'user',
            setup_roles_and_elements['roles']['user']
        )
        client = get_auth_client(user)

        response = client.get(reverse('orders-list-create'))

        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data

    def test_user_can_create_order(self, setup_roles_and_elements, create_user_with_role, get_auth_client):
        user = create_user_with_role(
            'user@test.com',
            'user',
            setup_roles_and_elements['roles']['user']
        )
        client = get_auth_client(user)

        data = {'product_id': 2, 'quantity': 1, 'total': 30000}
        response = client.post(reverse('orders-list-create'), data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['order']['owner_id'] == user.id


@pytest.mark.django_db
class TestGuestPermissions:
    def test_guest_can_read_products(self, setup_roles_and_elements, create_user_with_role, get_auth_client):
        guest = create_user_with_role(
            'guest@test.com',
            'guest',
            setup_roles_and_elements['roles']['guest']
        )
        client = get_auth_client(guest)

        response = client.get(reverse('products-list-create'))

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] >= 4

    def test_guest_cannot_create_product(self, setup_roles_and_elements, create_user_with_role, get_auth_client):
        guest = create_user_with_role(
            'guest@test.com',
            'guest',
            setup_roles_and_elements['roles']['guest']
        )
        client = get_auth_client(guest)

        data = {'name': 'Попытка гостя', 'price': 1000}
        response = client.post(reverse('products-list-create'), data, format='json')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_guest_cannot_access_orders(self, setup_roles_and_elements, create_user_with_role, get_auth_client):
        guest = create_user_with_role(
            'guest@test.com',
            'guest',
            setup_roles_and_elements['roles']['guest']
        )
        client = get_auth_client(guest)
        response = client.get(reverse('orders-list-create'))
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestUnauthorizedAccess:
    def test_anonymous_cannot_access_products(self, setup_roles_and_elements):
        client = APIClient()
        response = client.get(reverse('products-list-create'))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_anonymous_cannot_access_orders(self, setup_roles_and_elements):
        client = APIClient()
        response = client.get(reverse('orders-list-create'))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestMultipleRoles:
    def test_user_with_multiple_roles_has_combined_permissions(
            self, setup_roles_and_elements, create_user_with_role, get_auth_client
    ):
        user = User.objects.create_user(
            email='multirole@test.com',
            first_name='Multi',
            last_name='Role',
            password='testpass123'
        )
        user.is_verified = True
        user.save()

        UserRole.objects.create(user=user, role=setup_roles_and_elements['roles']['user'])
        UserRole.objects.create(user=user, role=setup_roles_and_elements['roles']['manager'])

        client = get_auth_client(user)

        response = client.get(reverse('orders-list-create'))
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] >= 3
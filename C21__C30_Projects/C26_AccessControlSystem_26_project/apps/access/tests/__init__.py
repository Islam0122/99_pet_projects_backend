import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.users.models import User, Role, UserRole
from apps.access.models import BusinessElement, AccessRolesRules


@pytest.fixture
def setup_admin_and_user(db):
    admin_role = Role.objects.create(name='admin', description='Администратор')
    user_role = Role.objects.create(name='user', description='Пользователь')

    admin = User.objects.create_user(
        email='admin@test.com',
        first_name='Admin',
        last_name='User',
        password='admin123'
    )
    admin.is_verified = True
    admin.save()
    UserRole.objects.create(user=admin, role=admin_role)

    regular_user = User.objects.create_user(
        email='user@test.com',
        first_name='Regular',
        last_name='User',
        password='user123'
    )
    regular_user.is_verified = True
    regular_user.save()
    UserRole.objects.create(user=regular_user, role=user_role)

    return {
        'admin': admin,
        'admin_role': admin_role,
        'user': regular_user,
        'user_role': user_role
    }


@pytest.fixture
def admin_client(setup_admin_and_user):
    client = APIClient()
    response = client.post(
        reverse('login'),
        {'email': 'admin@test.com', 'password': 'admin123'},
        format='json'
    )
    token = response.data['token']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return client


@pytest.fixture
def user_client(setup_admin_and_user):
    client = APIClient()
    response = client.post(
        reverse('login'),
        {'email': 'user@test.com', 'password': 'user123'},
        format='json'
    )
    token = response.data['token']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return client


@pytest.mark.django_db
class TestRoleManagement:
    def test_admin_can_list_roles(self, admin_client):
        response = admin_client.get(reverse('role-list'))

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 2  # admin и user

    def test_admin_can_create_role(self, admin_client):
        data = {
            'name': 'moderator',
            'description': 'Модератор системы'
        }

        response = admin_client.post(reverse('role-list'), data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'moderator'
        assert Role.objects.filter(name='moderator').exists()

    def test_admin_can_update_role(self, admin_client, setup_admin_and_user):
        role = setup_admin_and_user['user_role']

        data = {'description': 'Обновлённое описание'}
        response = admin_client.patch(
            reverse('role-detail', kwargs={'pk': role.id}),
            data,
            format='json'
        )

        assert response.status_code == status.HTTP_200_OK
        role.refresh_from_db()
        assert role.description == 'Обновлённое описание'

    def test_admin_can_delete_role(self, admin_client):
        role = Role.objects.create(name='temporary', description='Временная роль')

        response = admin_client.delete(reverse('role-detail', kwargs={'pk': role.id}))

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Role.objects.filter(id=role.id).exists()

    def test_regular_user_cannot_access_roles(self, user_client):
        response = user_client.get(reverse('role-list'))

        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestBusinessElementManagement:
    def test_admin_can_list_business_elements(self, admin_client):
        BusinessElement.objects.create(name='products', description='Товары')
        BusinessElement.objects.create(name='orders', description='Заказы')

        response = admin_client.get(reverse('business-element-list'))

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 2

    def test_admin_can_create_business_element(self, admin_client):
        data = {
            'name': 'invoices',
            'description': 'Счета-фактуры'
        }

        response = admin_client.post(
            reverse('business-element-list'),
            data,
            format='json'
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'invoices'

    def test_admin_can_update_business_element(self, admin_client):
        element = BusinessElement.objects.create(
            name='test_element',
            description='Тестовый элемент'
        )

        data = {'description': 'Обновлённое описание'}
        response = admin_client.patch(
            reverse('business-element-detail', kwargs={'pk': element.id}),
            data,
            format='json'
        )

        assert response.status_code == status.HTTP_200_OK
        element.refresh_from_db()
        assert element.description == 'Обновлённое описание'

    def test_regular_user_cannot_manage_business_elements(self, user_client):
        response = user_client.get(reverse('business-element-list'))

        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestAccessRulesManagement:
    def test_admin_can_list_access_rules(self, admin_client, setup_admin_and_user):
        role = setup_admin_and_user['admin_role']
        element = BusinessElement.objects.create(name='products', description='Товары')

        AccessRolesRules.objects.create(
            role=role,
            element=element,
            read_permission=True,
            read_all_permission=True,
            create_permission=True
        )

        response = admin_client.get(reverse('access-rule-list'))

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1

    def test_admin_can_create_access_rule(self, admin_client, setup_admin_and_user):
        role = setup_admin_and_user['user_role']
        element = BusinessElement.objects.create(name='orders', description='Заказы')

        data = {
            'role': role.id,
            'element': element.id,
            'read_permission': True,
            'read_all_permission': False,
            'create_permission': True,
            'update_permission': True,
            'update_all_permission': False,
            'delete_permission': False,
            'delete_all_permission': False
        }

        response = admin_client.post(
            reverse('access-rule-list'),
            data,
            format='json'
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['read_permission'] is True
        assert response.data['create_permission'] is True

    def test_admin_can_update_access_rule(self, admin_client, setup_admin_and_user):
        role = setup_admin_and_user['user_role']
        element = BusinessElement.objects.create(name='stores', description='Магазины')

        rule = AccessRolesRules.objects.create(
            role=role,
            element=element,
            read_permission=True,
            create_permission=False
        )

        data = {'create_permission': True}
        response = admin_client.patch(
            reverse('access-rule-detail', kwargs={'pk': rule.id}),
            data,
            format='json'
        )

        assert response.status_code == status.HTTP_200_OK
        rule.refresh_from_db()
        assert rule.create_permission is True

    def test_admin_can_delete_access_rule(self, admin_client, setup_admin_and_user):
        role = setup_admin_and_user['user_role']
        element = BusinessElement.objects.create(name='temp', description='Временный')

        rule = AccessRolesRules.objects.create(
            role=role,
            element=element,
            read_permission=True
        )

        response = admin_client.delete(
            reverse('access-rule-detail', kwargs={'pk': rule.id})
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not AccessRolesRules.objects.filter(id=rule.id).exists()


    def test_regular_user_cannot_manage_access_rules(self, user_client):
        response = user_client.get(reverse('access-rule-list'))

        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestRoleAssignment:

    def test_admin_can_assign_role_to_user(self, admin_client, setup_admin_and_user):
        new_user = User.objects.create_user(
            email='newuser@test.com',
            first_name='New',
            last_name='User',
            password='pass123'
        )
        new_user.is_verified = True
        new_user.save()

        manager_role = Role.objects.create(name='manager', description='Менеджер')

        data = {
            'user_id': new_user.id,
            'role_id': manager_role.id
        }

        response = admin_client.post(
            reverse('assign-role'),
            data,
            format='json'
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert UserRole.objects.filter(user=new_user, role=manager_role).exists()

    def test_admin_can_revoke_role_from_user(self, admin_client, setup_admin_and_user):
        user = setup_admin_and_user['user']
        role = setup_admin_and_user['user_role']

        data = {
            'user_id': user.id,
            'role_id': role.id
        }

        response = admin_client.post(
            reverse('revoke-role'),
            data,
            format='json'
        )

        assert response.status_code == status.HTTP_200_OK
        assert not UserRole.objects.filter(user=user, role=role).exists()

    def test_cannot_assign_duplicate_role(self, admin_client, setup_admin_and_user):
        user = setup_admin_and_user['user']
        role = setup_admin_and_user['user_role']

        data = {
            'user_id': user.id,
            'role_id': role.id
        }

        response = admin_client.post(
            reverse('assign-role'),
            data,
            format='json'
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'уже назначена' in str(response.data).lower()

    def test_cannot_revoke_nonexistent_role(self, admin_client, setup_admin_and_user):
        user = setup_admin_and_user['user']
        other_role = Role.objects.create(name='other', description='Другая роль')

        data = {
            'user_id': user.id,
            'role_id': other_role.id
        }

        response = admin_client.post(
            reverse('revoke-role'),
            data,
            format='json'
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_regular_user_cannot_assign_roles(self, user_client, setup_admin_and_user):
        data = {
            'user_id': 1,
            'role_id': 1
        }

        response = user_client.post(
            reverse('assign-role'),
            data,
            format='json'
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestMyPermissions:

    def test_user_can_view_own_permissions(self, user_client, setup_admin_and_user):
        user = setup_admin_and_user['user']
        role = setup_admin_and_user['user_role']
        element = BusinessElement.objects.create(name='products', description='Товары')

        AccessRolesRules.objects.create(
            role=role,
            element=element,
            read_permission=True,
            read_all_permission=True,
            create_permission=False
        )

        response = user_client.get(reverse('my-permissions'))

        assert response.status_code == status.HTTP_200_OK
        assert 'user' in response.data
        assert 'permissions' in response.data
        assert response.data['user']['email'] == 'user@test.com'

    def test_anonymous_cannot_view_permissions(self):
        client = APIClient()
        response = client.get(reverse('my-permissions'))

        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestAccessRulesValidation:

    def test_read_all_implies_read(self, admin_client, setup_admin_and_user):
        role = setup_admin_and_user['user_role']
        element = BusinessElement.objects.create(name='test', description='Test')

        data = {
            'role': role.id,
            'element': element.id,
            'read_permission': False,
            'read_all_permission': True,  # Включаем read_all
            'create_permission': False
        }

        response = admin_client.post(
            reverse('access-rule-list'),
            data,
            format='json'
        )

        assert response.status_code == status.HTTP_201_CREATED
        rule = AccessRolesRules.objects.get(id=response.data['id'])
        assert rule.read_permission is True

    def test_update_all_implies_update(self, admin_client, setup_admin_and_user):
        role = setup_admin_and_user['user_role']
        element = BusinessElement.objects.create(name='test', description='Test')

        data = {
            'role': role.id,
            'element': element.id,
            'read_permission': True,
            'update_permission': False,
            'update_all_permission': True
        }

        response = admin_client.post(
            reverse('access-rule-list'),
            data,
            format='json'
        )

        assert response.status_code == status.HTTP_201_CREATED
        rule = AccessRolesRules.objects.get(id=response.data['id'])
        assert rule.update_permission is True

    def test_unique_role_element_constraint(self, admin_client, setup_admin_and_user):
        role = setup_admin_and_user['user_role']
        element = BusinessElement.objects.create(name='unique_test', description='Test')

        AccessRolesRules.objects.create(
            role=role,
            element=element,
            read_permission=True
        )

        data = {
            'role': role.id,
            'element': element.id,
            'read_permission': True,
            'create_permission': True
        }

        response = admin_client.post(
            reverse('access-rule-list'),
            data,
            format='json'
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

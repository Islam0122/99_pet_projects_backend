from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import BusinessElement, AccessRolesRules
from apps.users.models import Role, UserRole
from .serializers import (
    BusinessElementSerializer,
    AccessRolesRulesSerializer,
    RoleSerializer,
    AssignRoleSerializer,
    RevokeRoleSerializer
)
from apps.users.permissions import IsAuthenticatedAndVerified


class IsAdmin(IsAuthenticatedAndVerified):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        return request.user.roles.filter(role__name='admin').exists()


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdmin]

    @action(detail=True, methods=['get'])
    def users(self, request, pk=None):
        role = self.get_object()
        user_roles = UserRole.objects.filter(role=role).select_related('user')
        users_data = [
            {
                'id': ur.user.id,
                'email': ur.user.email,
                'first_name': ur.user.first_name,
                'last_name': ur.user.last_name,
                'assigned_at': ur.assigned_at
            }
            for ur in user_roles
        ]
        return Response(users_data)


class BusinessElementViewSet(viewsets.ModelViewSet):
    queryset = BusinessElement.objects.all()
    serializer_class = BusinessElementSerializer
    permission_classes = [IsAdmin]


class AccessRolesRulesViewSet(viewsets.ModelViewSet):
    queryset = AccessRolesRules.objects.all().select_related('role', 'element')
    serializer_class = AccessRolesRulesSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        queryset = super().get_queryset()
        role_id = self.request.query_params.get('role_id')
        if role_id:
            queryset = queryset.filter(role_id=role_id)

        element_id = self.request.query_params.get('element_id')
        if element_id:
            queryset = queryset.filter(element_id=element_id)

        return queryset

    @action(detail=False, methods=['get'])
    def by_role(self, request):
        role_name = request.query_params.get('role_name')
        if not role_name:
            return Response(
                {"error": "Параметр role_name обязателен"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            role = Role.objects.get(name=role_name)
            rules = AccessRolesRules.objects.filter(role=role)
            serializer = self.get_serializer(rules, many=True)
            return Response(serializer.data)
        except Role.DoesNotExist:
            return Response(
                {"error": "Роль не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )


@api_view(['POST'])
@permission_classes([IsAdmin])
def assign_role(request):
    serializer = AssignRoleSerializer(data=request.data)
    if serializer.is_valid():
        user_role = serializer.save()
        return Response({
            "message": "Роль успешно назначена",
            "user_id": user_role.user.id,
            "user_email": user_role.user.email,
            "role_name": user_role.role.name,
            "assigned_at": user_role.assigned_at
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAdmin])
def revoke_role(request):
    serializer = RevokeRoleSerializer(data=request.data)
    if serializer.is_valid():
        user_role = serializer.validated_data['user_role']
        user_email = user_role.user.email
        role_name = user_role.role.name
        user_role.delete()
        return Response({
            "message": "Роль успешно отозвана",
            "user_email": user_email,
            "role_name": role_name
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticatedAndVerified])
def my_permissions(request):
    user = request.user
    user_roles = user.roles.all().values_list('role', flat=True)
    rules = AccessRolesRules.objects.filter(role_id__in=user_roles).select_related('role', 'element')

    permissions_by_element = {}
    for rule in rules:
        element_name = rule.element.name
        if element_name not in permissions_by_element:
            permissions_by_element[element_name] = {
                'element': element_name,
                'roles': [],
                'permissions': {
                    'read': False,
                    'read_all': False,
                    'create': False,
                    'update': False,
                    'update_all': False,
                    'delete': False,
                    'delete_all': False,
                }
            }

        permissions_by_element[element_name]['roles'].append(rule.role.name)

        perms = permissions_by_element[element_name]['permissions']
        perms['read'] = perms['read'] or rule.read_permission
        perms['read_all'] = perms['read_all'] or rule.read_all_permission
        perms['create'] = perms['create'] or rule.create_permission
        perms['update'] = perms['update'] or rule.update_permission
        perms['update_all'] = perms['update_all'] or rule.update_all_permission
        perms['delete'] = perms['delete'] or rule.delete_permission
        perms['delete_all'] = perms['delete_all'] or rule.delete_all_permission

    return Response({
        'user': {
            'id': user.id,
            'email': user.email,
            'roles': [ur.role.name for ur in user.roles.all()]
        },
        'permissions': list(permissions_by_element.values())
    })
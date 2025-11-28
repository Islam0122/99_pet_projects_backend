from rest_framework import serializers
from .models import BusinessElement, AccessRolesRules
from apps.users.models import Role, UserRole


class BusinessElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessElement
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['created_at']


class AccessRolesRulesSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.name', read_only=True)
    element_name = serializers.CharField(source='element.name', read_only=True)
    permissions_summary = serializers.CharField(source='get_permissions_summary', read_only=True)

    class Meta:
        model = AccessRolesRules
        fields = [
            'id',
            'role',
            'role_name',
            'element',
            'element_name',
            'read_permission',
            'read_all_permission',
            'create_permission',
            'update_permission',
            'update_all_permission',
            'delete_permission',
            'delete_all_permission',
            'permissions_summary',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, attrs):
        if attrs.get('read_all_permission') and not attrs.get('read_permission'):
            attrs['read_permission'] = True
        if attrs.get('update_all_permission') and not attrs.get('update_permission'):
            attrs['update_permission'] = True
        if attrs.get('delete_all_permission') and not attrs.get('delete_permission'):
            attrs['delete_permission'] = True

        return attrs


class RoleSerializer(serializers.ModelSerializer):
    users_count = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'users_count']

    def get_users_count(self, obj):
        return obj.users.count()


class AssignRoleSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    role_id = serializers.IntegerField(required=True)

    def validate_user_id(self, value):
        from apps.users.models import User
        if not User.objects.filter(id=value, is_active=True).exists():
            raise serializers.ValidationError("Пользователь не найден или неактивен")
        return value

    def validate_role_id(self, value):
        if not Role.objects.filter(id=value).exists():
            raise serializers.ValidationError("Роль не найдена")
        return value

    def validate(self, attrs):
        from apps.users.models import User
        user = User.objects.get(id=attrs['user_id'])
        role = Role.objects.get(id=attrs['role_id'])

        if UserRole.objects.filter(user=user, role=role).exists():
            raise serializers.ValidationError("Эта роль уже назначена пользователю")

        attrs['user'] = user
        attrs['role'] = role
        return attrs

    def create(self, validated_data):
        user_role = UserRole.objects.create(
            user=validated_data['user'],
            role=validated_data['role']
        )
        return user_role


class RevokeRoleSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    role_id = serializers.IntegerField(required=True)

    def validate(self, attrs):
        from apps.users.models import User
        try:
            user = User.objects.get(id=attrs['user_id'])
            role = Role.objects.get(id=attrs['role_id'])
        except (User.DoesNotExist, Role.DoesNotExist):
            raise serializers.ValidationError("Пользователь или роль не найдены")

        try:
            user_role = UserRole.objects.get(user=user, role=role)
            attrs['user_role'] = user_role
        except UserRole.DoesNotExist:
            raise serializers.ValidationError("У пользователя нет этой роли")

        return attrs
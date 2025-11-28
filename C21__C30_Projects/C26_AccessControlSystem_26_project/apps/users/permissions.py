from rest_framework import permissions
from apps.access.models import AccessRolesRules, BusinessElement


class IsAuthenticatedAndVerified(permissions.BasePermission):
    message = "Вы должны быть авторизованы и верифицированы"

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user and
            user.is_authenticated and
            user.is_active and
            getattr(user, 'is_verified', True)
        )


class RoleBasedPermission(permissions.BasePermission):
    message = "У вас нет прав для выполнения этого действия"

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated or not user.is_active:
            self.message = "Требуется аутентификация"
            return False

        element_name = getattr(view, 'business_element_name', None)
        if not element_name:
            return True

        action_type = getattr(view, 'action_type', None)
        if not action_type:
            return True

        try:
            element = BusinessElement.objects.get(name=element_name)
        except BusinessElement.DoesNotExist:
            self.message = f"Бизнес-элемент '{element_name}' не найден"
            return False

        user_role_ids = user.roles.all().values_list('role_id', flat=True)
        if not user_role_ids:
            self.message = "У вас нет назначенных ролей"
            return False

        rules = AccessRolesRules.objects.filter(
            role_id__in=user_role_ids,
            element_id=element.id
        )

        if not rules.exists():
            self.message = f"Нет правил доступа для элемента '{element_name}'"
            return False

        check_owner = getattr(view, 'check_owner', False)
        obj = None

        if check_owner and hasattr(view, 'get_object'):
            try:
                obj = view.get_object()
            except Exception:
                obj = None

        for rule in rules:
            if self._check_rule_permission(rule, action_type, user, obj, check_owner):
                return True

        self.message = f"У вас нет прав для действия '{action_type}' на элементе '{element_name}'"
        return False

    def _check_rule_permission(self, rule, action_type, user, obj, check_owner):
        if action_type == "read":
            if rule.read_all_permission:
                return True
            if rule.read_permission and not check_owner:
                return True
            if rule.read_permission and check_owner and obj and hasattr(obj, 'owner_id'):
                return obj.owner_id == user.id

        elif action_type == "create":
            return rule.create_permission

        elif action_type == "update":
            if rule.update_all_permission:
                return True
            if rule.update_permission and not check_owner:
                return True
            if rule.update_permission and check_owner and obj and hasattr(obj, 'owner_id'):
                return obj.owner_id == user.id

        elif action_type == "delete":
            if rule.delete_all_permission:
                return True
            if rule.delete_permission and not check_owner:
                return True
            if rule.delete_permission and check_owner and obj and hasattr(obj, 'owner_id'):
                return obj.owner_id == user.id

        return False


class IsOwner(permissions.BasePermission):
    message = "Вы не являетесь владельцем этого объекта"

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        if hasattr(obj, 'owner_id'):
            return obj.owner_id == request.user.id
        if hasattr(obj, 'user'):
            return obj.user == request.user
        if hasattr(obj, 'user_id'):
            return obj.user_id == request.user.id
        return False


class IsAdminRole(permissions.BasePermission):
    message = "Требуются права администратора"

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return user.roles.filter(role__name='admin').exists()


class IsManagerRole(permissions.BasePermission):
    message = "Требуются права менеджера или администратора"

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return user.roles.filter(role__name__in=['admin', 'manager']).exists()
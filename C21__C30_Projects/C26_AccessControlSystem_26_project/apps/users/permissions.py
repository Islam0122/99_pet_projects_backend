from rest_framework import permissions
from apps.access.models import AccessRolesRules, BusinessElement


class IsAuthenticatedAndVerified(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.is_active and user.is_verified)


class RoleBasedPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated or not user.is_active:
            return False

        element_name = getattr(view, 'business_element_name', None)
        if not element_name:
            return False

        action_type = getattr(view, 'action_type', None)
        if not action_type:
            return False

        try:
            element = BusinessElement.objects.get(name=element_name)
        except BusinessElement.DoesNotExist:
            return False

        roles = user.roles.all().values_list('role_id', flat=True)
        rules = AccessRolesRules.objects.filter(role_id__in=roles, element_id=element.id)
        if not rules.exists():
            return False

        check_owner = getattr(view, 'check_owner', False)
        obj = getattr(view, 'get_object', lambda: None)()
        for rule in rules:
            if action_type == "read":
                if rule.read_all_permission or (rule.read_permission and (not check_owner or obj.owner_id == user.id)):
                    return True
            elif action_type == "create":
                if rule.create_permission:
                    return True
            elif action_type == "update":
                if rule.update_all_permission or (
                        rule.update_permission and (not check_owner or obj.owner_id == user.id)):
                    return True
            elif action_type == "delete":
                if rule.delete_all_permission or (
                        rule.delete_permission and (not check_owner or obj.owner_id == user.id)):
                    return True
        return False

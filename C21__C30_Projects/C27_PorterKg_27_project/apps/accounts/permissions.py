from rest_framework.permissions import BasePermission


class IsDriver(BasePermission):
    """
    Разрешение только для водителей
    """

    def has_permission(self, request, view):
        return (
                request.user and
                request.user.is_authenticated and
                request.user.role in ['driver', 'admin']
        )


class IsGuest(BasePermission):
    """
    Разрешение только для гостей
    """

    def has_permission(self, request, view):
        return (
                request.user and
                request.user.is_authenticated and
                request.user.role in ['guest', 'admin']
        )


class IsOwnerOrReadOnly(BasePermission):
    """
    Разрешение на изменение только для владельца объекта
    """

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        return obj.user == request.user


class IsVerifiedDriver(BasePermission):
    """
    Разрешение только для верифицированных водителей
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.role != 'driver':
            return False

        try:
            return request.user.driver_profile.verified_driver
        except AttributeError:
            return False


class IsAdmin(BasePermission):
    """
    Разрешение только для администраторов
    """

    def has_permission(self, request, view):
        return (
                request.user and
                request.user.is_authenticated and
                request.user.role == 'admin'
        )
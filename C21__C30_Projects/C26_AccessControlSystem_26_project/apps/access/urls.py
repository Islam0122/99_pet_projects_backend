from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RoleViewSet,
    BusinessElementViewSet,
    AccessRolesRulesViewSet,
    assign_role,
    revoke_role,
    my_permissions
)

router = DefaultRouter()
router.register('roles', RoleViewSet, basename='role')
router.register('business-elements', BusinessElementViewSet, basename='business-element')
router.register('access-rules', AccessRolesRulesViewSet, basename='access-rule')

urlpatterns = [
    path('', include(router.urls)),
    path('assign-role/', assign_role, name='assign-role'),
    path('revoke-role/', revoke_role, name='revoke-role'),
    path('my-permissions/', my_permissions, name='my-permissions'),
]
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GroupViewSet, StudentViewSet

router = DefaultRouter()
router.register(r'groups', GroupViewSet)
router.register(r'students', StudentViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Все API будет доступно под /api/
]

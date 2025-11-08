from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TGUserViewSet

router = DefaultRouter()
router.register(r"telegram-users", TGUserViewSet, basename="telegram-user")

urlpatterns = [
    path("", include(router.urls)),
]

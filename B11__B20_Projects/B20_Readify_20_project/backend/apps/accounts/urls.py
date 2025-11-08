from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TGUserViewSet, TGUserTOPViewSet

router = DefaultRouter()
router.register(r"telegram-users", TGUserViewSet, basename="telegram-user")
router.register(r"telegram-top", TGUserTOPViewSet, basename="telegram-top")

urlpatterns = [
    path("", include(router.urls)),
]

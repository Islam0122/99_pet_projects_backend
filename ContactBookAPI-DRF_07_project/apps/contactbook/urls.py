from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactBookViewSet

router = DefaultRouter()
router.register(r'contacts', ContactBookViewSet, basename='contacts')

urlpatterns = [
    path('', include(router.urls)),
]

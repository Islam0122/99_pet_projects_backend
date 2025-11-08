from django.urls import path, include
from rest_framework import routers
from .views import ProductViewSet,CategoryViewSet

router = routers.DefaultRouter()
router.register('category', CategoryViewSet)
router.register('product', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TimerViewSet, CategoryViewSet, TextViewSet

router = DefaultRouter()
router.register(r'timers', TimerViewSet, basename='timer')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'texts', TextViewSet, basename='text')

urlpatterns = [
    path('', include(router.urls)),
]

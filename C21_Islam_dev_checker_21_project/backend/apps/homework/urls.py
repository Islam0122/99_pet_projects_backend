from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import Month1HomeworkViewSet, Month2HomeworkViewSet, Month3HomeworkViewSet

router = DefaultRouter()
router.register(r'month1', Month1HomeworkViewSet, basename='month1-homework')
router.register(r'month2', Month2HomeworkViewSet, basename='month2-homework')
router.register(r'month3', Month3HomeworkViewSet, basename='month3-homework')

urlpatterns = [
    path('', include(router.urls)),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResultsTestViewSet

router = DefaultRouter()
router.register(r'tests', ResultsTestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

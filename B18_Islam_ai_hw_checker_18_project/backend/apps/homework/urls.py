from rest_framework.routers import DefaultRouter
from .views import HomeWorkViewSet

router = DefaultRouter()
router.register(r'homework', HomeWorkViewSet, basename='homework')

urlpatterns = router.urls

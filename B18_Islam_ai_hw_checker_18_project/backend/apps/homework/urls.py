from rest_framework.routers import DefaultRouter
from .views import HomeWorkViewSet,StudentRead

router = DefaultRouter()
router.register(r'homework', HomeWorkViewSet, basename='homework')
router.register(r'student', StudentRead, basename='student')

urlpatterns = router.urls

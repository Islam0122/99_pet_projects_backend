from rest_framework.routers import DefaultRouter
from .views import TgUserViewSet

router = DefaultRouter()
router.register(r'tg-users', TgUserViewSet, basename='tguser')

urlpatterns = router.urls

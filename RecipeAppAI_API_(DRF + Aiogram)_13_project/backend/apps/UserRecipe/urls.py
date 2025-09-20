from rest_framework.routers import DefaultRouter
from .views import UserRecipeViewSet

router = DefaultRouter()
router.register(r"user-recipes", UserRecipeViewSet, basename="user-recipe")

urlpatterns = router.urls

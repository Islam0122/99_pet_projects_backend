from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LinkViewSet, redirect_link

router = DefaultRouter()
router.register(r"api/shorten", LinkViewSet, basename="link")

urlpatterns = [
    path('api/', include(router.urls)),
    path('r/<str:short_code>/', redirect_link, name='redirect-link'),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, TagViewSet, QuoteViewSet

router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'tags', TagViewSet)
router.register(r'quotes', QuoteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TopicViewSet, QuestionViewSet


router = DefaultRouter()
router.register(r'topics', TopicViewSet)  # /api/topics/
router.register(r'questions', QuestionViewSet)  # /api/questions/

# Добавляем маршруты в urlpatterns
urlpatterns = [
    path('', include(router.urls)),  # Включаем все маршруты
]

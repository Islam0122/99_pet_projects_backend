from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LevelViewSet , QuestionViewSet ,TestViewSet, ResultsTestViewSet,PlacementTestViewSet

router = DefaultRouter()
router.register(r'levels', LevelViewSet, basename='level')
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'tests', TestViewSet, basename='test')
router.register(r'results', ResultsTestViewSet, basename='results')
router.register(r'placement-tests', PlacementTestViewSet, basename='placement-test')


urlpatterns = [
    path('', include(router.urls)),

]

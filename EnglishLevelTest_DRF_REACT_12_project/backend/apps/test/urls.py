from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (LevelViewSet , QuestionViewSet ,TestViewSet, ResultsTestViewSet,
                    PlacementTestViewSet,PlacementTestResultViewSet)

router = DefaultRouter()
router.register(r'levels', LevelViewSet, basename='level')
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'tests', TestViewSet, basename='test')
router.register(r'results', ResultsTestViewSet, basename='results')
router.register(r'placement-tests', PlacementTestViewSet, basename='placement-test')
router.register(r'placement-tests-results', PlacementTestResultViewSet, basename='placement-tests-results')

urlpatterns = [
    path('', include(router.urls)),

]

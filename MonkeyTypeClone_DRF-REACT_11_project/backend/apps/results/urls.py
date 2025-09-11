from django.urls import path
from .views import TestResultCreateView, MyTestResultsView, LeaderboardView

urlpatterns = [
    path("test-results/", TestResultCreateView.as_view(), name="test-result-create"),
    path("test-results/me/", MyTestResultsView.as_view(), name="my-test-results"),
    path("leaderboard/", LeaderboardView.as_view(), name="leaderboard"),
]
from django.utils import timezone
from datetime import timedelta

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import TestResult
from .serializers import TestResultSerializer, LeaderboardSerializer
from ..user.models import User


# ------------------------------
#  Сохранение результата теста
# ------------------------------
@extend_schema(
    summary="Сохранить результат теста",
    description="Сохраняет результат теста для текущего авторизованного пользователя",
    request=TestResultSerializer,
    responses={201: TestResultSerializer},
    tags=["TestResult"]

)
class TestResultCreateView(generics.CreateAPIView):
    serializer_class = TestResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ------------------------------
#  Мои результаты
# ------------------------------
@extend_schema(
    summary="Моя история тестов",
    description="Возвращает список всех тестов, которые прошёл текущий пользователь",
    responses={200: TestResultSerializer(many=True)},
    tags=["MyTestResults"]

)
class MyTestResultsView(generics.ListAPIView):
    serializer_class = TestResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TestResult.objects.filter(user=self.request.user)


# ------------------------------
#  Лидерборд
# ------------------------------
@extend_schema(
    summary="Лидерборд",
    description="Топ игроков по WPM. Можно выбрать период: daily, weekly, monthly, all",
    parameters=[
        OpenApiParameter(
            name="period",
            description="Период лидерборда",
            required=False,
            type=str,
            enum=["daily", "weekly", "monthly", "all"],
            default="all",
        )
    ],
    responses={200: LeaderboardSerializer(many=True)},
    tags=["Leaderboard"]
)
class LeaderboardView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        period = request.query_params.get("period", "all")

        qs = User.objects.all()
        now = timezone.now()

        if period == "daily":
            since = now - timedelta(days=1)
            qs = qs.filter(test_results__created_at__gte=since)
        elif period == "weekly":
            since = now - timedelta(weeks=1)
            qs = qs.filter(test_results__created_at__gte=since)
        elif period == "monthly":
            since = now - timedelta(days=30)
            qs = qs.filter(test_results__created_at__gte=since)

        qs = qs.distinct().order_by("-best_wpm")[:20]
        serializer = LeaderboardSerializer(qs, many=True)
        return Response(serializer.data)

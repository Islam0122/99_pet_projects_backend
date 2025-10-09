from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from .models import TGUser
from .serializers import TGUserSerializer


class TGUserViewSet(viewsets.ModelViewSet):
    queryset = TGUser.objects.all().order_by("-created_at")
    serializer_class = TGUserSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        "telegram_id": ["exact"],
        "username": ["icontains"],
        "streak_days": ["gte", "lte"],
        "created_at": ["date__gte", "date__lte"],
    }
    search_fields = ["username", "telegram_id"]
    ordering_fields = ["streak_days", "total_task_completes", "created_at"]
    ordering = ["-streak_days"]

    def perform_create(self, serializer):
        tg_id = self.request.data.get("telegram_id")
        username = self.request.data.get("username", "")
        instance, created = TGUser.objects.get_or_create(
            telegram_id=tg_id,
            defaults={"username": username},
        )
        if not created:
            instance.username = username
            instance.save()
        return instance

from rest_framework import viewsets, filters
from .models import TgUser
from .serializers import TgUserSerializer

class TgUserViewSet(viewsets.ModelViewSet):
    queryset = TgUser.objects.all()
    serializer_class = TgUserSerializer

    # Поддержка поиска и сортировки
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["username", "full_name"]
    ordering_fields = ["created_at", "username"]
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = super().get_queryset()
        telegram_id = self.request.query_params.get("telegram_id")
        if telegram_id:
            queryset = queryset.filter(telegram_id=telegram_id)
        return queryset
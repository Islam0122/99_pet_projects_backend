from rest_framework import viewsets, filters
from .models import TgUser
from .serializers import TgUserSerializer

class TgUserViewSet(viewsets.ModelViewSet):
    queryset = TgUser.objects.all()
    serializer_class = TgUserSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["username", "full_name", "telegram_id"]
    ordering_fields = ["created_at", "username"]
    ordering = ["-created_at"]

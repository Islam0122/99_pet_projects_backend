from rest_framework import viewsets, filters
from .models import TgUser
from .serializers import TgUserSerializer
from django.core.cache import cache

class TgUserViewSet(viewsets.ModelViewSet):
    queryset = TgUser.objects.all()
    serializer_class = TgUserSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["username", "full_name"]
    ordering_fields = ["created_at", "username"]
    ordering = ["-created_at"]

    def get_queryset(self):
        telegram_id = self.request.query_params.get("telegram_id")
        if telegram_id:
            cache_key = f"tg_user:{telegram_id}"
            user = cache.get(cache_key)
            if user:
                return TgUser.objects.filter(id=user['id'])

            queryset = super().get_queryset().filter(telegram_id=telegram_id)
            if queryset.exists():
                user_data = {
                    'id': queryset.first().id,
                    'username': queryset.first().username,
                    'full_name': queryset.first().full_name,
                    'telegram_id': queryset.first().telegram_id,
                }
                cache.set(cache_key, user_data, timeout=60)  # кэш на 60 секунд
            return queryset

        return super().get_queryset()

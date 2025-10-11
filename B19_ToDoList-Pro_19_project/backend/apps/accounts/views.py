from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
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

    def create(self, request, *args, **kwargs):
        tg_id = request.data.get("telegram_id")
        if not tg_id:
            return Response({"telegram_id": "Это поле обязательно."}, status=status.HTTP_400_BAD_REQUEST)

        username = request.data.get("username", "")
        instance, created = TGUser.objects.get_or_create(
            telegram_id=tg_id,
            defaults={"username": username},
        )

        if not created and instance.username != username:
            instance.username = username
            instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

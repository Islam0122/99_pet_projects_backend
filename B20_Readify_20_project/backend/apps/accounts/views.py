from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from datetime import timedelta
from .models import TGUser
from .serializers import TGUserSerializer


class TGUserTOPViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TGUserSerializer
    permission_classes = [AllowAny]
    lookup_field = "telegram_id"

    def get_queryset(self):
        return TGUser.objects.all().order_by("-xp")[:10]


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
    ordering_fields = ["streak_days", "created_at"]
    ordering = ["-streak_days"]
    lookup_field = "telegram_id"

    def create(self, request, *args, **kwargs):
        tg_id = request.data.get("telegram_id")
        if not tg_id:
            return Response(
                {"telegram_id": "Это поле обязательно."},
                status=status.HTTP_400_BAD_REQUEST
            )

        username = request.data.get("username", "")
        instance, created = TGUser.objects.get_or_create(
            telegram_id=tg_id,
            defaults={"username": username},
        )

        if not created and instance.username != username:
            instance.username = username
            instance.save()

        serializer = self.get_serializer(instance)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def update_books_read(self, request, telegram_id=None):
        """Обновление счетчика прочитанных книг и проверка streak"""
        try:
            user = self.get_object()

            # Увеличиваем счетчик прочитанных книг
            user.total_read_books += 1

            # Проверяем и обновляем streak
            today = timezone.now().date()
            yesterday = today - timedelta(days=1)

            if user.last_read_date == yesterday:
                # Пользователь читал вчера - увеличиваем streak
                user.streak_days += 1
            elif user.last_read_date != today:
                # Пользователь не читал вчера - сбрасываем streak
                user.streak_days = 1

            # Обновляем дату последнего чтения
            user.last_read_date = today
            user.save()

            return Response({
                "message": "Статистика обновлена",
                "total_read_books": user.total_read_books,
                "streak_days": user.streak_days,
                "last_read_date": user.last_read_date,
                "streak_status": user.streak_status,
                "level": user.level,
                "rank": user.rank
            })

        except TGUser.DoesNotExist:
            return Response(
                {"error": "Пользователь не найден"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"Ошибка при обновлении статистики: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def add_xp(self, request, telegram_id=None):
        """Добавление XP пользователю"""
        try:
            user = self.get_object()
            xp_amount = request.data.get('xp_amount', 0)

            if not isinstance(xp_amount, int) or xp_amount <= 0:
                return Response(
                    {"error": "xp_amount должен быть положительным числом"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Добавляем XP (автоматически обновит уровень и звание)
            user.add_xp(xp_amount)

            return Response({
                "message": f"Добавлено {xp_amount} XP",
                "xp": user.xp,
                "level": user.level,
                "rank": user.rank
            })

        except TGUser.DoesNotExist:
            return Response(
                {"error": "Пользователь не найден"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"Ошибка при добавлении XP: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['get'])
    def stats(self, request, telegram_id=None):
        """Получение полной статистики пользователя"""
        try:
            user = self.get_object()
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        except TGUser.DoesNotExist:
            return Response(
                {"error": "Пользователь не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['get'])
    def leaderboard(self, request):
        """Таблица лидеров по разным параметрам"""
        try:
            # Топ по XP
            xp_leaders = TGUser.objects.all().order_by('-xp')[:10]
            xp_serializer = self.get_serializer(xp_leaders, many=True)

            # Топ по streak
            streak_leaders = TGUser.objects.all().order_by('-streak_days')[:10]
            streak_serializer = self.get_serializer(streak_leaders, many=True)

            # Топ по прочитанным книгам
            books_leaders = TGUser.objects.all().order_by('-total_read_books')[:10]
            books_serializer = self.get_serializer(books_leaders, many=True)

            return Response({
                "by_xp": xp_serializer.data,
                "by_streak": streak_serializer.data,
                "by_books": books_serializer.data
            })

        except Exception as e:
            return Response(
                {"error": f"Ошибка при получении таблицы лидеров: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
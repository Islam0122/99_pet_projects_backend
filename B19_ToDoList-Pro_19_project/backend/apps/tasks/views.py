from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task, Category
from .serializers import TaskSerializer, CategorySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .tasks import send_task_reminders

@api_view(['POST'])
def test_send_reminders(request):
    send_task_reminders.delay()
    return Response({"status": "Celery task triggered"})


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["done", "categories"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "due_date"]
    ordering = ["-created_at"]

    def perform_update(self, serializer):
        serializer.save()

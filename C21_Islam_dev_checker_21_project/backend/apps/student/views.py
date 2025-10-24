from django.db import models
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Group, Student
from .serializers import GroupSerializer, StudentSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления учебными группами.
    Поиск и работа происходит через telegram_id.
    """
    queryset = Group.objects.all().prefetch_related("students")
    serializer_class = GroupSerializer
    lookup_field = "telegram_id"
    lookup_url_kwarg = "telegram_id"

    @action(detail=True, methods=["get"], url_path="students")
    def students(self, request, telegram_id=None):
        """
        Получить всех студентов группы по telegram_id.
        Пример: /api/groups/<telegram_id>/students/
        """
        group = self.get_object()
        students = group.students.all().order_by("full_name")
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StudentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления студентами.
    Поиск и работа через telegram_id.
    """
    queryset = Student.objects.select_related("group").all()
    serializer_class = StudentSerializer
    lookup_field = "telegram_id"
    lookup_url_kwarg = "telegram_id"

    @action(detail=False, methods=["get"], url_path="active")
    def active_students(self, request):
        """
        Возвращает всех активных студентов.
        Пример: /api/students/active/
        """
        students = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="progress")
    def progress(self, request, telegram_id=None):
        """
        Возвращает прогресс конкретного студента по telegram_id.
        Пример: /api/students/<telegram_id>/progress/
        """
        student = self.get_object()
        progress = {
            "full_name": student.full_name,
            "group": student.group.title if student.group else None,
            "progress_percent": (
                (student.completed_homeworks / student.total_homeworks) * 100
                if student.total_homeworks else 0
            ),
            "average_score": student.average_score,
            "best_score": student.best_score,
            "rank": student.rank,
            "progress_level": student.progress_level,
        }
        return Response(progress, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="top")
    def top_students(self, request):
        """
        Возвращает топ-5 студентов по среднему баллу.
        Пример: /api/students/top/
        """
        limit = int(request.query_params.get("limit", 5))  # можно задать ?limit=10
        top_students = Student.objects.order_by("-average_score")[:limit]
        serializer = self.get_serializer(top_students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="stats")
    def stats(self, request):
        """
        Общая статистика по всем студентам.
        Пример: /api/students/stats/
        """
        data = Student.objects.aggregate(
            total_students=models.Count("id"),
            total_homeworks=models.Sum("total_homeworks"),
            average_score=models.Avg("average_score"),
        )
        return Response(data, status=status.HTTP_200_OK)

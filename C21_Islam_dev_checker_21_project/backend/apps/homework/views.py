from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import *
from .serializers import *
from ..student.models import Student
from .services.homework_checker import sent_prompt_and_get_response, extract_grade_from_feedback


from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import Month1HomeworkSerializer, Month1HomeworkItemSerializer
from .models import Month1Homework, Month1HomeworkItem
from ..student.models import Student
from .services.homework_checker import sent_prompt_and_get_response, extract_grade_from_feedback


class Month1HomeworkViewSet(viewsets.ModelViewSet):
    queryset = Month1Homework.objects.select_related("student").prefetch_related("items").order_by("-created_at")
    serializer_class = Month1HomeworkSerializer

    def get_queryset(self):
        """
        Фильтрация по имени студента или уроку через query-параметры.
        Пример: /api/month1_homeworks/?student=1&lesson=ООП
        """
        queryset = super().get_queryset()
        student_id = self.request.query_params.get("student")
        lesson = self.request.query_params.get("lesson")

        if student_id:
            queryset = queryset.filter(student=student_id)

        if lesson:
            queryset = queryset.filter(lesson=lesson)

        return queryset

    def create(self, request, *args, **kwargs):
        student_id = request.data.get("student")
        lesson = request.data.get("lesson")
        tasks = request.data.get("tasks")

        if not all([student_id, lesson, tasks]) or not isinstance(tasks, list):
            return Response(
                {"error": "Все поля обязательны: student, lesson, tasks (список)"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        student = get_object_or_404(Student, id=student_id)

        # Проверка: студент может отправить домашку только один раз
        if Month1Homework.objects.filter(student=student, lesson=lesson).exists():
            return Response(
                {"error": f"Вы уже отправили домашку по уроку '{lesson}'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Создаем запись домашки
        homework = Month1Homework.objects.create(student=student, lesson=lesson)
        items_data = []

        for task in tasks:
            task_condition = task.get("task_condition")
            student_answer = task.get("student_answer")
            if not all([task_condition, student_answer]):
                continue

            # AI проверка
            prompt_review = f"""
Ты — Islam Teacher AI. Проверь домашнее задание студента.
Имя: {student.full_name}
Условие: {task_condition}
Ответ: {student_answer}
"""
            prompt_originality = f"""
Ты — Islam Teacher AI. Определи, использовал ли студент искусственный интеллект.
Ответь строго "Да" или "Нет".
Ответ студента: {student_answer}
"""

            ai_feedback = sent_prompt_and_get_response(prompt_review)
            originality_check = sent_prompt_and_get_response(prompt_originality)
            grade = extract_grade_from_feedback(ai_feedback) or 7

            # Создаем пункт задания
            item = Month1HomeworkItem.objects.create(
                homework=homework,
                task_condition=task_condition,
                student_answer=student_answer,
                grade=grade,
                ai_feedback=ai_feedback,
                originality_check=originality_check,
            )
            items_data.append(Month1HomeworkItemSerializer(item).data)

        serializer = Month1HomeworkSerializer(homework)
        data = serializer.data
        data["items"] = items_data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="recheck")
    def recheck_homework(self, request, pk=None):
        """
        Переоценка домашнего задания вручную (повторная проверка AI)
        """
        homework = self.get_object()
        updated_items = []

        for item in homework.items.all():
            prompt_review = f"""
Ты — Islam Teacher AI. Проверь задание студента повторно.
Условие: {item.task_condition}
Ответ: {item.student_answer}
"""
            ai_feedback = sent_prompt_and_get_response(prompt_review)
            originality_check = sent_prompt_and_get_response(
                f"Определи, использовал ли студент AI. Ответь 'Да' или 'Нет'. Ответ: {item.student_answer}"
            )
            grade = extract_grade_from_feedback(ai_feedback) or 7

            item.grade = grade
            item.ai_feedback = ai_feedback
            item.originality_check = originality_check
            item.save()

            updated_items.append(Month1HomeworkItemSerializer(item).data)

        serializer = Month1HomeworkSerializer(homework)
        data = serializer.data
        data["items"] = updated_items
        return Response(data, status=status.HTTP_200_OK)


class Month2HomeworkViewSet(viewsets.ModelViewSet):
    queryset = Month2Homework.objects.select_related("student").order_by("-created_at")
    serializer_class = Month2HomeworkSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        student_id = self.request.query_params.get("student")
        lesson = self.request.query_params.get("lesson")
        if student_id:
            queryset = queryset.filter(student=student_id)
        if lesson:
            queryset = queryset.filter(lesson=lesson)
        return queryset

    def create(self, request, *args, **kwargs):
        student_id = request.data.get("student")
        lesson = request.data.get("lesson")
        title = request.data.get("title")
        task_condition = request.data.get("task_condition")

        if not all([student_id, lesson, title, task_condition]):
            return Response(
                {"error": "Все поля обязательны: student, lesson, title, task_condition"},
                status=status.HTTP_400_BAD_REQUEST
            )

        student = get_object_or_404(Student, id=student_id)

        if Month2Homework.objects.filter(student=student, lesson=lesson).exists():
            return Response(
                {"error": f"Вы уже создали домашку по уроку '{lesson}'"},
                status=status.HTTP_400_BAD_REQUEST
            )

        homework = Month2Homework.objects.create(
            student=student,
            lesson=lesson,
            title=title,
            task_condition=task_condition
        )
        serializer = Month2HomeworkSerializer(homework)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class Month3HomeworkViewSet(viewsets.ModelViewSet):
    queryset = Month3Homework.objects.select_related("student").order_by("-created_at")
    serializer_class = Month3HomeworkSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        student_id = self.request.query_params.get("student")
        lesson = self.request.query_params.get("lesson")
        if student_id:
            queryset = queryset.filter(student=student_id)
        if lesson:
            queryset = queryset.filter(lesson=lesson)
        return queryset

    def create(self, request, *args, **kwargs):
        student_id = request.data.get("student")
        lesson = request.data.get("lesson")
        title = request.data.get("title")
        task_condition = request.data.get("task_condition")

        if not all([student_id, lesson, title, task_condition]):
            return Response(
                {"error": "Все поля обязательны: student, lesson, title, task_condition"},
                status=status.HTTP_400_BAD_REQUEST
            )

        student = get_object_or_404(Student, id=student_id)

        if Month3Homework.objects.filter(student=student, lesson=lesson).exists():
            return Response(
                {"error": f"Вы уже создали домашку по уроку '{lesson}'"},
                status=status.HTTP_400_BAD_REQUEST
            )

        homework = Month3Homework.objects.create(
            student=student,
            lesson=lesson,
            title=title,
            task_condition=task_condition
        )
        serializer = Month3HomeworkSerializer(homework)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


from django.db import transaction
from django.utils import timezone

from .serializers import *
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import Month1HomeworkSerializer, Month1HomeworkItemSerializer
from .models import Month1Homework, Month1HomeworkItem, MONTH_1_LESSONS as TASK_1_MONTH_LESSON_CHOICES
from ..student.models import Student
from .services.homework_checker import sent_prompt_and_get_response, extract_grade_from_feedback
import re


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

        # Проверка существования студента
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return Response(
                {"error": "Студент не найден"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Проверка валидности урока
        valid_lessons = [choice[0] for choice in TASK_1_MONTH_LESSON_CHOICES]
        if lesson not in valid_lessons:
            return Response(
                {"error": f"Неверный урок. Допустимые значения: {', '.join(valid_lessons)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Проверка существования домашней работы
        if Month1Homework.objects.filter(student=student, lesson=lesson).exists():
            return Response(
                {"error": f"Вы уже отправили домашку по уроку '{lesson}'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Валидация tasks
        valid_tasks = []
        for i, task in enumerate(tasks):
            task_condition = task.get("task_condition", "").strip()
            student_answer = task.get("student_answer", "").strip()

            if not task_condition:
                return Response(
                    {"error": f"Задание {i + 1}: условие задания обязательно"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not student_answer:
                return Response(
                    {"error": f"Задание {i + 1}: ответ студента обязателен"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            valid_tasks.append({
                "task_condition": task_condition,
                "student_answer": student_answer
            })

        # Создание в транзакции
        with transaction.atomic():
            homework = Month1Homework.objects.create(student=student, lesson=lesson)
            items_data = []

            for task in valid_tasks:
                try:
                    # AI проверка с таймаутом
                    prompt_review = f"""
                    Ты — Islam Teacher AI.

                    Задача: проверить домашнюю работу студента **строго по шаблону ниже**.

                    ---
                    ## Анализ домашнего задания

                    ### Задание:
                    «{task['task_condition']}»

                    ### Решение студента:
                    «{task['student_answer']}»
                    ---

                    **Анализ решения:**
                    - **Понятность:** оцени, насколько ясно студент выразил мысль.
                    - **Логика:** оцени, есть ли связь между условием и ответом.
                    - **Правильность:** напиши, верно ли решено задание.
                    - **Структура:** оцени оформление и наличие объяснений.
                    - **Качество:** общая оценка качества работы.

                    ---

                    ## Итоговая оценка

                    ОЦЕНКА: X  
                    Комментарий: Кратко объясни причину выставленной оценки.
                    ---

                    ⚠️ Формат должен строго сохраняться.  
                    ⚠️ Вместо X обязательно поставь конкретную цифру от 0 до 10.
                    """

                    ai_feedback = self._get_ai_response_safe(prompt_review)
                    originality_check = self._get_ai_response_safe(
                        f"Определи, использовал ли студент ИИ для выполнения задания. Ответ студента: {task['student_answer']}. Ответь только 'Да' или 'Нет'."
                    )
                    grade = self._extract_grade_safe(ai_feedback)

                    item = Month1HomeworkItem.objects.create(
                        homework=homework,
                        task_condition=task['task_condition'],
                        student_answer=task['student_answer'],
                        grade=grade,
                        ai_feedback=ai_feedback,
                        originality_check=originality_check,
                        is_checked=True,
                        checked_at=timezone.now()
                    )
                    items_data.append(Month1HomeworkItemSerializer(item).data)

                except Exception as e:
                    # Если AI проверка не удалась, создаем запись без проверки
                    item = Month1HomeworkItem.objects.create(
                        homework=homework,
                        task_condition=task['task_condition'],
                        student_answer=task['student_answer'],
                        ai_feedback="Ошибка при проверке AI",
                        originality_check="Не проверено",
                        is_checked=False
                    )
                    items_data.append(Month1HomeworkItemSerializer(item).data)

        serializer = Month1HomeworkSerializer(homework)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _get_ai_response_safe(self, prompt):
        """Безопасный запрос к AI с таймаутом"""
        try:
            # Добавьте таймаут для избежания долгих запросов
            return sent_prompt_and_get_response(prompt)
        except Exception:
            return "Не удалось получить ответ от AI"

    def _extract_grade_safe(self, ai_feedback: str):
        try:
            # Ищем строку вроде: ОЦЕНКА: **10**
            match = re.search(r"ОЦЕНКА[:\s\*]+(\d+)", ai_feedback)
            if match:
                return int(match.group(1))
        except Exception:
            pass
        return 0

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

    @action(detail=False, methods=['get'], url_path='student/(?P<student_id>\d+)')
    def get_student_homeworks(self, request, student_id=None):
        """Получить все домашние работы конкретного студента"""
        homeworks = self.get_queryset().filter(student_id=student_id)
        serializer = self.get_serializer(homeworks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='lessons')
    def get_available_lessons(self, request):
        """Получить список доступных уроков"""
        lessons = [{"value": choice[0], "label": choice[1]}
                   for choice in TASK_1_MONTH_LESSON_CHOICES]
        return Response(lessons)

    @action(detail=True, methods=['patch'], url_path='update-grade')
    def update_grade(self, request, pk=None):
        """Ручное обновление оценки преподавателем"""
        homework = self.get_object()
        item_id = request.data.get('item_id')
        new_grade = request.data.get('grade')

        if not all([item_id, new_grade]):
            return Response(
                {"error": "item_id и grade обязательны"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            item = homework.items.get(id=item_id)
            item.grade = max(0, min(10, float(new_grade)))  # Ограничение 0-10
            item.is_checked = True
            item.checked_at = timezone.now()
            item.save()

            return Response(Month1HomeworkItemSerializer(item).data)
        except Month1HomeworkItem.DoesNotExist:
            return Response(
                {"error": "Задание не найдено"},
                status=status.HTTP_404_NOT_FOUND
            )


class Month2HomeworkViewSet(viewsets.ModelViewSet):
    queryset = Month2Homework.objects.select_related("student").order_by("-created_at")
    serializer_class = Month2HomeworkSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        student_id = self.request.query_params.get("student")
        lesson = self.request.query_params.get("lesson")
        is_checked = self.request.query_params.get("is_checked")

        if student_id:
            queryset = queryset.filter(student_id=student_id)
        if lesson:
            queryset = queryset.filter(lesson=lesson)
        if is_checked is not None:
            # Конвертируем "true"/"false" в bool
            is_checked_bool = is_checked.lower() == "true"
            queryset = queryset.filter(is_checked=is_checked_bool)

        return queryset

    def create(self, request, *args, **kwargs):
        student_id = request.data.get("student")
        lesson = request.data.get("lesson")
        title = request.data.get("title")
        task_condition = request.data.get("task_condition")
        github_url = request.data.get("github_url")

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
            task_condition=task_condition,
            github_url=github_url
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
        is_checked = self.request.query_params.get("is_checked")

        if student_id:
            queryset = queryset.filter(student_id=student_id)
        if lesson:
            queryset = queryset.filter(lesson=lesson)
        if is_checked is not None:
            # Конвертируем "true"/"false" в bool
            is_checked_bool = is_checked.lower() == "true"
            queryset = queryset.filter(is_checked=is_checked_bool)

        return queryset

    def create(self, request, *args, **kwargs):
        student_id = request.data.get("student")
        lesson = request.data.get("lesson")
        title = request.data.get("title")
        task_condition = request.data.get("task_condition")
        github_url = request.data.get("github_url")

        if not all([student_id, lesson, title, task_condition, github_url]):
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
            task_condition=task_condition,
            github_url=github_url
        )
        serializer = Month3HomeworkSerializer(homework)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



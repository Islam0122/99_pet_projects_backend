from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import HomeWork, HwItem, Student
from .serializers import HomeWorkSerializer, HwItemSerializer, StudentSerializer
from .services.homework_checker import sent_prompt_and_get_response, extract_grade_from_feedback
from rest_framework.decorators import action


class StudentRead(viewsets.ReadOnlyModelViewSet):
    """Позволяет просматривать список студентов и проверять, существует ли студент."""
    queryset = Student.objects.all().order_by("name")
    serializer_class = StudentSerializer

    @action(detail=False, methods=["get"], url_path="check")
    def check_student(self, request):
        """
        Проверяет, существует ли студент по имени и email.
        Пример: /api/students/check/?name=Islam&email=example@gmail.com
        Возвращает { "exists": true } или { "exists": false }
        """
        name = request.query_params.get("name")
        email = request.query_params.get("email")

        if not name or not email:
            return Response(
                {"error": "Параметры name и email обязательны"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        exists = Student.objects.filter(name__iexact=name, email__iexact=email).exists()
        return Response({"exists": exists})




class HomeWorkViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с домашними заданиями.
    - GET: просмотр списка/одного задания
    - POST: создание с AI-проверкой
    """
    queryset = HomeWork.objects.select_related("student").prefetch_related("items").order_by("-created_at")
    serializer_class = HomeWorkSerializer

    def get_queryset(self):
        """
        Фильтрация по имени студента или уроку через query-параметры.
        Пример: /api/homeworks/?student_name=Islam&lesson=ООП
        """
        queryset = super().get_queryset()
        student_name = self.request.query_params.get("student_name")
        lesson = self.request.query_params.get("lesson")

        if student_name:
            queryset = queryset.filter(student__name__icontains=student_name)

        if lesson:
            queryset = queryset.filter(lesson=lesson)

        return queryset

    def create(self, request, *args, **kwargs):
        """
        Создание домашнего задания с проверкой AI.
        Ожидается JSON:
        {
            "student_email": "...",
            "lesson": "...",
            "tasks": [
                {"task_condition": "...", "student_answer": "..."},
                ...
            ]
        }
        """
        student_email = request.data.get("student_email")
        lesson = request.data.get("lesson")
        tasks = request.data.get("tasks")

        # Проверяем входные данные
        if not all([student_email, lesson, tasks]) or not isinstance(tasks, list):
            return Response(
                {"error": "Все поля обязательны: student_email, lesson, tasks (список)"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Ищем или создаём студента
        student, _ = Student.objects.get_or_create(email=student_email, defaults={"name": request.data.get("student_name", "Без имени")})

        # Проверяем, отправлял ли уже студент домашку по этому уроку
        if HomeWork.objects.filter(student=student, lesson=lesson).exists():
            return Response(
                {"error": f"Вы уже отправили домашку по уроку '{lesson}'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Создаём запись домашнего задания
        homework = HomeWork.objects.create(student=student, lesson=lesson)
        items_data = []

        for task in tasks:
            task_condition = task.get("task_condition")
            student_answer = task.get("student_answer")

            if not all([task_condition, student_answer]):
                continue  # пропускаем неполные задания

            # --- AI проверка ---
            prompt_review = f"""
Ты — Islam Teacher AI. Проверь домашнее задание студента.
Имя: {student.name}
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
            grade = extract_grade_from_feedback(ai_feedback) or 7  # по умолчанию 7, если не найдено

            item = HwItem.objects.create(
                homework=homework,
                task_condition=task_condition,
                student_answer=student_answer,
                grade=grade,
                ai_feedback=ai_feedback,
                originality_check=originality_check,
            )
            items_data.append(HwItemSerializer(item).data)

        # Ответ клиенту
        serializer = HomeWorkSerializer(homework)
        data = serializer.data
        data["items"] = items_data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="recheck")
    def recheck_homework(self, request, pk=None):
        """
        Переоценка домашнего задания вручную.
        Можно вызывать для повторной проверки AI.
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

            updated_items.append(HwItemSerializer(item).data)

        serializer = HomeWorkSerializer(homework)
        data = serializer.data
        data["items"] = updated_items
        return Response(data, status=status.HTTP_200_OK)

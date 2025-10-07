from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import HomeWork, HwItem
from .serializers import HomeWorkSerializer, HwItemSerializer
from .services.homework_checker import sent_prompt_and_get_response, extract_grade_from_feedback


class HomeWorkViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с домашними заданиями.
    GET - просмотр
    POST - создание с AI-проверкой
    """
    queryset = HomeWork.objects.all().order_by("-created_at")
    serializer_class = HomeWorkSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        student_name = self.request.query_params.get("student_name")
        lesson = self.request.query_params.get("lesson")
        if student_name:
            queryset = queryset.filter(student_name__icontains=student_name)
        if lesson:
            queryset = queryset.filter(lesson=lesson)
        return queryset

    def create(self, request, *args, **kwargs):
        """
        Создание домашки с проверкой AI.
        Студент может отправить домашку по одному уроку только один раз.
        """
        student_name = request.data.get("student_name")
        student_email = request.data.get("student_email")
        lesson = request.data.get("lesson")
        tasks = request.data.get("tasks")

        if not all([student_name, student_email, lesson, tasks]) or not isinstance(tasks, list):
            return Response(
                {"error": "Все поля обязательны: student_name, student_email, lesson, tasks (список)"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Проверяем, есть ли уже отправка по этому уроку
        if HomeWork.objects.filter(student_name=student_name, lesson=lesson).exists():
            return Response(
                {"error": f"Вы уже отправили домашку по уроку '{lesson}'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Создаём HomeWork
        homework = HomeWork.objects.create(
            student_name=student_name,
            student_email=student_email,
            lesson=lesson,
        )

        items_data = []
        for task in tasks:
            task_condition = task.get("task_condition")
            student_answer = task.get("student_answer")
            if not all([task_condition, student_answer]):
                continue

            # AI проверка
            prompt_review = f"""
    Ты — islam teacher ai. Проверь домашнее задание студента.
    Имя: {student_name}
    Условие: {task_condition}
    Ответ: {student_answer}
    """
            prompt_originality = f"""
    Ты — islam teacher ai. Проверь, использовал ли студент AI.
    Ответь строго "Да" или "Нет".
    Ответ студента: {student_answer}
    """
            ai_feedback = sent_prompt_and_get_response(prompt_review)
            originality_check = sent_prompt_and_get_response(prompt_originality)
            grade = extract_grade_from_feedback(ai_feedback)

            item = HwItem.objects.create(
                homework=homework,
                task_condition=task_condition,
                student_answer=student_answer,
                grade=grade if grade else 7,
                ai_feedback=ai_feedback,
                originality_check=originality_check,
            )
            items_data.append(HwItemSerializer(item).data)

        serializer = HomeWorkSerializer(homework)
        data = serializer.data
        data["items"] = items_data
        return Response(data, status=status.HTTP_201_CREATED)

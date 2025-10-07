from django.db import models


class HomeWork(models.Model):
    LESSON_CHOICES = [
        ("Введение в Python", "Введение в Python. Переменные, типы данных"),
        ("Условные конструкции", "Условные конструкции (if, else, elif)"),
        ("Циклы", "Циклы for, while"),
        ("Списки", "Списки, срезы, кортежи"),
        ("Словари и множества", "Словари, множества"),
        ("Функции", "Функции, *args, **kwargs"),
        ("Lambda и исключения", "Lambda, исключения"),
        ("Файлы", "Работа с файлами (txt, JSON, CSV)"),
        ("Алгоритмы", "Основы алгоритмов (поиск, сортировка)"),
        ("Мини проект", "Практика: консольное приложение"),
        ("ООП", "Введение в ООП. Классы и объекты"),
        ("Атрибуты и методы", "Атрибуты и методы"),
        ("Наследование", "Наследование, полиморфизм, инкапсуляция"),
        ("Магические методы", "Магические методы"),
        ("RPG проект", "Практика: RPG Game"),
        ("Модули", "Встроенные и собственные модули"),
        ("Окружения", "Виртуальные окружения"),
        ("Регулярки", "Регулярные выражения"),
        ("Финальный проект", "Итоговый проект месяца"),
    ]

    student_name = models.CharField(
        max_length=100,
        verbose_name="Имя ученика",
        help_text="Введите имя и фамилию ученика"
    )
    student_email = models.EmailField(
        verbose_name="Электронная почта ученика",
        help_text="Введите e-mail ученика"
    )
    lesson = models.CharField(
        max_length=100,
        choices=LESSON_CHOICES,
        verbose_name="Урок",
        help_text="Выберите урок, к которому относится задание"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    def __str__(self):
        return f"{self.student_name} ({self.lesson})"

    class Meta:
        verbose_name = "Результат задания"
        verbose_name_plural = "Результаты заданий"
        ordering = ["-created_at"]


class HwItem(models.Model):
    homework = models.ForeignKey(
        HomeWork,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Домашняя работа"
    )
    task_condition = models.TextField(
        verbose_name="Условие задания",
        help_text="Введите условие задания, данное ученику"
    )
    student_answer = models.TextField(
        verbose_name="Ответ ученика",
        help_text="Введите ответ ученика"
    )
    grade = models.FloatField(
        verbose_name="Оценка (из 10)",
        help_text="Введите оценку за задание (от 0 до 10)",
        null=True,
        blank=True
    )
    ai_feedback = models.TextField(
        verbose_name="Комментарий от Islam AI Checker",
        help_text="Комментарий, сгенерированный системой Islam AI Checker",
        null=True,
        blank=True
    )
    originality_check = models.TextField(
        verbose_name="Анализ оригинальности",
        help_text="Проверка, сам ли ученик выполнил задание или использовал AI",
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Задание ({self.homework.lesson}) — {self.homework.student_name}"

    class Meta:
        verbose_name = "Пункт задания"
        verbose_name_plural = "Пункты заданий"
        ordering = ["id"]

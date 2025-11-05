from django.db import models
from ..student.models import Student

MONTH_1_LESSONS = [
    ("День 1", "Введение в Python. Переменные, типы данных"),
    ("День 2", "Условные конструкции (if, else, elif)"),
    ("День 3", "Циклы for, while"),
    ("День 4", "Списки, срезы, кортежи"),
    ("День 5", "Словари, множества"),
    ("День 6", "Функции. Аргументы (*args, **kwargs)"),
    ("День 7", "Lambda, исключения"),
    ("День 8", "Работа с файлами (txt, JSON, CSV)"),
    ("День 9", "Основы алгоритмов (поиск, сортировка)"),
    ("День 10", "Практика: мини-проект (консольное приложение)"),
    ("День 11", "Введение в ООП. Классы и объекты"),
    ("День 12", "Атрибуты и методы"),
    ("День 13", "Наследование, полиморфизм, инкапсуляция"),
    ("День 14", "Магические методы"),
    ("День 15", "Практика: проект на ООП RPG Game"),
    ("День 16", "Встроенные модули Python, собственные модули, виртуальные окружения"),
    ("День 17", "Git/GitHub: команды"),
    ("День 18", "Введение в Flask, установка, первый маршрут Hello"),
    ("День 19", "Маршруты + шаблоны (Jinja2)"),
    ("День 20", "Формы и POST-запросы / Итоговый проект месяца (мини-система)")
]

MONTH_2_LESSONS = [
    ("День 1", "Работа с базой данных (SQLite)"),
    ("День 2", "CRUD-операции"),
    ("День 3", "Шаблоны и Bootstrap"),
    ("День 4", "Авторизация (базовая)"),
    ("День 5", "Деплой проекта / Мини-проект"),
    ("День 6", "Создание первого бота, настройка токена"),
    ("День 7", "Обработка сообщений и команд"),
    ("День 8", "Кнопки (Reply и Inline)"),
    ("День 9", "FSM: состояния и хранение данных"),
    ("День 10", "Подключение базы данных (SQLite)"),
    ("День 11", "Интеграция БД с ботом"),
    ("День 12", "FSMAdmin, админ-панель"),
    ("День 13", "Практика: бот-магазин (без оплаты)"),
    ("День 14", "Работа с API (requests)"),
    ("День 15", "Web scraping (BS4)"),
    ("День 16", "Планировщик задач (Aioschedule)"),
    ("День 17", "Middleware, фильтры, флаги"),
    ("День 18", "Git/GitHub: деплой на сервер (Heroku/VPS)"),
    ("День 19", "Практика: деплой Telegram-бота"),
    ("День 20", "Итоговый проект месяца (командная работа) / Презентация проектов")
]

MONTH_3_LESSONS = [
    ("День 1", "Введение в Django. Структура проекта"),
    ("День 2", "Первые view, urls"),
    ("День 3", "Django templates / HTML, CSS"),
    ("День 4", "Модели и база данных"),
    ("День 5", "Практика: блог (CRUD)"),
    ("День 6", "Class Based Views, Django Forms"),
    ("День 7", "Django Admin, суперпользователь"),
    ("День 8", "Request/Response в Django"),
    ("День 9", "Аутентификация и авторизация"),
    ("День 10", "Практика: сайт-магазин"),
    ("День 11", "Django Rest Framework: APIView"),
    ("День 12", "Сериализаторы, валидация данных"),
    ("День 13", "Class Based Views и mixins в DRF"),
    ("День 14", "ViewSets, routers, пагинация"),
    ("День 15", "Практика: API для интернет-магазина"),
    ("День 16", "Аутентификация и разрешения в DRF"),
    ("День 17", "Тестирование (pytest, unittest)"),
    ("День 18", "Документация API (Swagger)"),
    ("День 19", "Итоговый проект Bootcamp (сайт / API / бот)"),
    ("День 20", "Защита финальных проектов")
]




# === 1 МЕСЯЦ ===
class Month1Homework(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="month1_homeworks",
        verbose_name="Студент",
    )
    lesson = models.CharField(
        max_length=100,
        choices=MONTH_1_LESSONS,
        verbose_name="Урок",
        help_text="Выберите урок, к которому относится задание",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"{self.student.full_name} — {self.lesson}"

    def save(self, *args, **kwargs):
        """Переопределяем save, чтобы обновлять прогресс студента после сохранения"""
        super().save(*args, **kwargs)
        if self.student:
            self.student.update_progress(month=1)

    class Meta:
        verbose_name = "Домашняя работа (1 месяц)"
        verbose_name_plural = "Домашние работы (1 месяц)"
        ordering = ["-created_at"]


class Month1HomeworkItem(models.Model):
    homework = models.ForeignKey(
        Month1Homework,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Домашняя работа",
    )
    task_condition = models.TextField(
        verbose_name="Условие задания",
        help_text="Введите условие задания, данное ученику",
    )
    student_answer = models.TextField(
        verbose_name="Ответ ученика",
        help_text="Введите ответ ученика",
        blank=True,
        null=True,
    )
    grade = models.FloatField(
        verbose_name="Оценка (из 10)",
        help_text="Введите оценку за задание (от 0 до 10)",
        null=True,
        blank=True,
    )
    ai_feedback = models.TextField(
        verbose_name="Комментарий от Islam AI Checker",
        help_text="Комментарий, сгенерированный системой Islam AI Checker",
        null=True,
        blank=True,
    )
    originality_check = models.TextField(
        verbose_name="Анализ оригинальности",
        help_text="Проверка, сам ли ученик выполнил задание или использовал AI",
        null=True,
        blank=True,
    )
    is_checked = models.BooleanField(default=False, verbose_name="Проверено",null=True,
        blank=True)

    checked_at = models.DateTimeField(
        verbose_name="Время проверки",
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Обновляем прогресс студента каждый раз, когда меняется grade или проверка
        if self.homework.student:
            self.homework.student.update_progress(month=1)

    def __str__(self):
        return f"Задание: {self.homework.lesson} — {self.homework.student.full_name}"

    class Meta:
        verbose_name = "Пункт задания (1 месяц)"
        verbose_name_plural = "Пункты заданий (1 месяц)"
        ordering = ["id"]


# === 2 МЕСЯЦ ===
class Month2Homework(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="month2_homeworks",
        verbose_name="Студент",
    )
    lesson = models.CharField(
        max_length=100,
        choices=MONTH_2_LESSONS,
        verbose_name="Урок",
        help_text="Выберите урок, к которому относится задание",
    )
    title = models.CharField(max_length=255, verbose_name="Название задания")
    task_condition = models.TextField(verbose_name="Условие задания")
    grade = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Оценка (из 10)",
    )
    originality_check = models.TextField(
        null=True,
        blank=True,
        verbose_name="Проверка оригинальности",
    )
    is_checked = models.BooleanField(default=False, verbose_name="Проверено")
    github_url = models.URLField(blank=True, null=True, verbose_name="GitHub URL")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"{self.student.full_name} — {self.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.student:
            self.student.update_progress(month=2)


    class Meta:
        verbose_name = "Домашняя работа (2 месяц)"
        verbose_name_plural = "Домашние работы (2 месяц)"
        ordering = ["-created_at"]


# === 3 МЕСЯЦ ===
class Month3Homework(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="month3_homeworks",
        verbose_name="Студент",
    )
    title = models.CharField(max_length=255, verbose_name="Название задания")
    lesson = models.CharField(
        max_length=100,
        choices=MONTH_3_LESSONS,
        verbose_name="Урок",
        help_text="Выберите урок, к которому относится задание",
    )
    task_condition = models.TextField(verbose_name="Условие задания")
    grade = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Оценка (из 10)",
    )
    originality_check = models.TextField(
        null=True,
        blank=True,
        verbose_name="Проверка оригинальности",
    )
    is_checked = models.BooleanField(default=False, verbose_name="Проверено")
    github_url = models.URLField(blank=True, null=True, verbose_name="GitHub URL")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"{self.student.full_name} — {self.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.student:
            self.student.update_progress(month=3)


    class Meta:
        verbose_name = "Домашняя работа (3 месяц)"
        verbose_name_plural = "Домашние работы (3 месяц)"
        ordering = ["-created_at"]
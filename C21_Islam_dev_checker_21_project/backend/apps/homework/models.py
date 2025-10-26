from django.db import models
from ..student.models import Student

TASK_1_MONTH_LESSON_CHOICES = [
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
TASK_2_MONTH_LESSON_CHOICES = [
    ("Создание первого бота", "lesson 1: Настройка токена и создание первого бота"),
    ("Обработка сообщений и команд", "lesson 2: Основы обработки сообщений и команд"),
    ("Кнопки (Reply и Inline)", "lesson 3: Добавление кнопок Reply и Inline"),
    ("FSM: состояния и хранение данных", "lesson 4: Состояния и хранение данных"),
    ("Практика: бот-анкета", "lesson 5: Практическая работа — бот анкета"),
    ("Подключение базы данных (SQLite)", "lesson 6: Подключение базы данных"),
    ("CRUD-операции в БД", "lesson 7: Создание, чтение, обновление, удаление"),
    ("Интеграция БД с ботом", "lesson 8: Связь бота с базой данных"),
    ("FSMAdmin, админ-панель", "lesson 9: Работа с FSMAdmin и админкой"),
    ("Практика: бот-магазин (без оплаты)", "lesson 10: Практика — магазин бот"),
    ("Работа с API (requests)", "lesson 11: Использование API"),
    ("Web scraping (BS4)", "lesson 12: Сбор данных с веб-сайтов"),
    ("Планировщик задач (Aioschedule)", "lesson 13: Настройка планировщика задач"),
    ("Middleware, фильтры, флаги", "lesson 14: Настройка Middleware и фильтров"),
    ("Практика: бот-новостник или бот-напоминалка", "lesson 15: Практическая работа"),
    ("Git/GitHub --> command", "lesson 16: Основы Git"),
    ("Git/GitHub / Деплой на сервер (Heroku/VPS)", "lesson 17: Деплой проекта"),
    ("Практика: деплой Telegram-бота", "lesson 18: Практическая работа"),
    ("Итоговый проект месяца (командная работа)", "lesson 19: Командная работа"),
    ("Презентация проектов", "lesson 20: Презентация результатов"),
]
TASK_3_MONTH_LESSON_CHOICES = [
    ("Введение в Django", "lesson 1: Структура проекта"),
    ("Первые view, urls", "lesson 2: Создание view и маршрутов"),
    ("Django templates / html / css", "lesson 3: Работа с шаблонами"),
    ("Модели и база данных", "lesson 4: Создание моделей и миграций"),
    ("Практика: блог (CRUD)", "lesson 5: Практическая работа — блог"),
    ("Class Based Views, Django Forms", "lesson 6: Работа с CBV и формами"),
    ("Django Admin, суперпользователь", "lesson 7: Настройка админки"),
    ("Request/Response в Django", "lesson 8: Основы Request и Response"),
    ("Аутентификация и авторизация", "lesson 9: Пользователи и права"),
    ("Практика: сайт-магазин", "lesson 10: Практическая работа — магазин"),
    ("Django Rest Framework. APIView", "lesson 11: Создание API с DRF"),
    ("Сериализаторы, валидация данных", "lesson 12: Работа с сериализаторами"),
    ("Class Based Views и mixins в DRF", "lesson 13: CBV и миксины"),
    ("ViewSets, routers, пагинация", "lesson 14: ViewSets и маршрутизация"),
    ("Практика: API для интернет-магазина", "lesson 15: Практическая работа"),
    ("Аутентификация и разрешения в DRF", "lesson 16: Права доступа"),
    ("Тестирование (pytest, unittest)", "lesson 17: Тестирование API"),
    ("Документация API (Swagger)", "lesson 18: Документирование API"),
    ("Итоговый проект Bootcamp (сайт or API or бот)", "lesson 19: Финальный проект"),
    ("Защита финальных проектов", "lesson 20: Презентация проектов"),
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
        choices=TASK_1_MONTH_LESSON_CHOICES,
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
    is_checked = models.BooleanField(default=False, verbose_name="Проверено")

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
        choices=TASK_2_MONTH_LESSON_CHOICES,
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
        choices=TASK_3_MONTH_LESSON_CHOICES,
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
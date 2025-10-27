from django.db import models


class Group(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Название группы",
        help_text="Введите название учебной группы (например: Python 101)",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание группы",
        help_text="Краткое описание или дополнительная информация о группе",
    )
    telegram_id = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="ID Telegram-группы",
        help_text="Введите уникальный Telegram ID группы",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"
        ordering = ["title"]


class Student(models.Model):
    full_name = models.CharField(
        max_length=100,
        verbose_name="Полное имя",
        help_text="Введите имя и фамилию студента",
    )
    username = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Имя пользователя в Telegram",
        help_text="Укажите Telegram username (без @), если есть",
    )
    telegram_id = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="ID Telegram пользователя",
        help_text="Введите уникальный Telegram ID студента",
    )
    group = models.ForeignKey(
        "Group",
        on_delete=models.CASCADE,
        related_name="students",
        verbose_name="Группа",
        help_text="Выберите группу, в которой учится студент",
    )

    total_homeworks = models.PositiveIntegerField(
        default=0,
        verbose_name="Всего домашних заданий",
    )
    completed_homeworks = models.PositiveIntegerField(
        default=0,
        verbose_name="Выполненные задания",
    )
    last_homework_done = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Последнее выполненное задание",
    )
    average_score = models.FloatField(
        default=0.0,
        verbose_name="Средний балл",
    )
    best_score = models.FloatField(
        default=0.0,
        verbose_name="Лучший балл",
    )
    total_points = models.FloatField(
        default=0.0,
        verbose_name="Общее количество баллов",
    )
    rank = models.PositiveIntegerField(
        default=0,
        verbose_name="Рейтинг в группе",
    )
    progress_level = models.CharField(
        max_length=50,
        default="Новичок",
        verbose_name="Уровень прогресса",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен",
    )

    # ---------- Вспомогательные методы ----------
    def calculate_progress_level(self) -> str:
        """Вычисляет уровень прогресса по проценту выполнения"""
        if self.total_homeworks == 0:
            return "Новичок"

        completion_rate = (self.completed_homeworks / self.total_homeworks) * 100
        if completion_rate < 20:
            return "Новичок"
        elif completion_rate < 40:
            return "Начинающий"
        elif completion_rate < 60:
            return "Средний"
        elif completion_rate < 80:
            return "Продвинутый"
        return "Лидер"

    def calculate_scores(self, homeworks):
        """Обновляет статистику студента по списку домашних заданий"""
        self.total_homeworks = homeworks.count()
        checked_homeworks = homeworks.filter(is_checked=True)

        self.completed_homeworks = checked_homeworks.count()
        self.total_points = sum(hw.grade or 0 for hw in checked_homeworks)
        self.average_score = (
            self.total_points / self.completed_homeworks if self.completed_homeworks else 0.0
        )
        self.best_score = max((hw.grade or 0 for hw in checked_homeworks), default=0)
        self.progress_level = self.calculate_progress_level()

    # ---------- Методы обновления ----------
    def update_progress(self,month):
        """Пересчитывает статистику студента сразу по всем месяцам (Duolingo-стиль)"""

        all_homeworks = []

        # Month1
        for hw in getattr(self, "month1_homeworks").all():
            all_homeworks += list(hw.items.filter(is_checked=True))

        # Month2
        all_homeworks += list(getattr(self, "month2_homeworks").filter(is_checked=True))

        # Month3
        all_homeworks += list(getattr(self, "month3_homeworks").filter(is_checked=True))

        self.total_homeworks = (
                self.month1_homeworks.count() +
                self.month2_homeworks.count() +
                self.month3_homeworks.count()
        )

        self.completed_homeworks = len(all_homeworks)
        self.total_points = sum(getattr(hw, "grade", 0) or 0 for hw in all_homeworks)
        self.average_score = (
            self.total_points / self.completed_homeworks if self.completed_homeworks else 0.0
        )
        self.best_score = max(
            ((getattr(hw, "grade", 0) or 0) for hw in all_homeworks),
            default=0
        )

        # Прогресс как процент выполнения
        if self.total_homeworks == 0:
            self.progress_level = "Новичок"
        else:
            completion_rate = (self.completed_homeworks / self.total_homeworks) * 100
            if completion_rate < 20:
                self.progress_level = "Новичок"
            elif completion_rate < 40:
                self.progress_level = "Начинающий"
            elif completion_rate < 60:
                self.progress_level = "Средний"
            elif completion_rate < 80:
                self.progress_level = "Продвинутый"
            else:
                self.progress_level = "Лидер"

        super(Student, self).save(update_fields=[
            "total_homeworks",
            "completed_homeworks",
            "total_points",
            "average_score",
            "best_score",
            "progress_level",
        ])

    # ---------- Переопределение save ----------
    def save(self, *args, **kwargs):
        # Пересчитать уровень прогресса
        self.progress_level = self.calculate_progress_level()

        # Средний балл
        if self.completed_homeworks > 0:
            self.average_score = self.total_points / self.completed_homeworks
        else:
            self.average_score = 0.0

        # Лучший балл - только если объект уже сохранен
        if self.pk:  # ← ДОБАВЬТЕ ЭТУ ПРОВЕРКУ
            related_homeworks = []
            for month in range(1, 13):
                relation = f"month{month}_homeworks"
                if hasattr(self, relation):
                    try:
                        related_homeworks += list(getattr(self, relation).filter(is_checked=True))
                    except ValueError:
                        # Игнорируем ошибку если объект еще не сохранен
                        continue

            if related_homeworks:
                self.best_score = max(hw.grade or 0 for hw in related_homeworks)
            else:
                self.best_score = 0.0
        else:
            # Для новых объектов устанавливаем best_score в 0
            self.best_score = 0.0

        super().save(*args, **kwargs)

        # Пересчёт рейтинга в группе (этот код остается, он работает после сохранения)
        students_in_group = Student.objects.filter(group=self.group).order_by(
            "-total_points", "full_name"
        )
        for idx, student in enumerate(students_in_group, start=1):
            if student.rank != idx:
                Student.objects.filter(pk=student.pk).update(rank=idx)
    def __str__(self):
        return f"{self.full_name} ({self.group.title})"

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"
        ordering = ["full_name"]


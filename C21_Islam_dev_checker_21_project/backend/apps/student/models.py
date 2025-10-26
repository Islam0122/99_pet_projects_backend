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
        help_text="Общее количество заданий, выданных студенту",
    )
    completed_homeworks = models.PositiveIntegerField(
        default=0,
        verbose_name="Выполненные задания",
        help_text="Количество заданий, успешно выполненных студентом",
    )
    last_homework_done = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Последнее выполненное задание",
        help_text="Дата и время последнего выполненного задания",
    )
    average_score = models.FloatField(
        default=0.0,
        verbose_name="Средний балл",
        help_text="Средний балл по всем сданным заданиям",
    )
    best_score = models.FloatField(
        default=0.0,
        verbose_name="Лучший балл",
        help_text="Максимальный балл, полученный студентом за домашние задания",
    )
    total_points = models.FloatField(
        default=0.0,
        verbose_name="Общее количество баллов",
        help_text="Сумма всех полученных баллов студента",
    )
    rank = models.PositiveIntegerField(
        default=0,
        verbose_name="Рейтинг в группе",
        help_text="Позиция студента в рейтинге группы",
    )
    progress_level = models.CharField(
        max_length=50,
        default="Новичок",
        verbose_name="Уровень прогресса",
        help_text="Статус студента: например, 'Новичок', 'Продвинутый', 'Лидер'",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен",
        help_text="Отображает, активен ли студент в учебной программе",
    )

    def save(self, *args, **kwargs):
        if self.total_homeworks == 0:
            level = "Новичок"
        else:
            completion_rate = (self.completed_homeworks / self.total_homeworks) * 100
            if completion_rate < 20:
                level = "Новичок"
            elif completion_rate < 40:
                level = "Начинающий"
            elif completion_rate < 60:
                level = "Средний"
            elif completion_rate < 80:
                level = "Продвинутый"
            else:
                level = "Лидер"

        if self.progress_level != level:
            self.progress_level = level

        if self.completed_homeworks > 0:
            self.average_score = self.total_points / self.completed_homeworks
        else:
            self.average_score = 0.0
        if self.best_score < self.average_score:
            self.best_score = self.average_score

        super().save(*args, **kwargs)

        students_in_group = Student.objects.filter(group=self.group).order_by('-total_points', 'full_name')
        for idx, student in enumerate(students_in_group, start=1):
            if student.rank != idx:
                Student.objects.filter(pk=student.pk).update(rank=idx)

    def __str__(self):
        return f"{self.full_name} ({self.group.title})"


    def update_progress(self):
        homeworks = self.month3_homeworks.all()  # все домашки студента
        self.total_homeworks = homeworks.count()
        self.completed_homeworks = homeworks.filter(is_checked=True).count()
        self.total_points = sum(hw.grade or 0 for hw in homeworks if hw.is_checked)

        # Средний балл
        if self.completed_homeworks > 0:
            self.average_score = self.total_points / self.completed_homeworks
        else:
            self.average_score = 0.0

        # Лучший балл
        self.best_score = max((hw.grade or 0 for hw in homeworks if hw.is_checked), default=0)

        # Обновляем уровень прогресса
        if self.total_homeworks == 0:
            level = "Новичок"
        else:
            completion_rate = (self.completed_homeworks / self.total_homeworks) * 100
            if completion_rate < 20:
                level = "Новичок"
            elif completion_rate < 40:
                level = "Начинающий"
            elif completion_rate < 60:
                level = "Средний"
            elif completion_rate < 80:
                level = "Продвинутый"
            else:
                level = "Лидер"

        self.progress_level = level
        self.save(update_fields=[
            "total_homeworks", "completed_homeworks", "total_points",
            "average_score", "best_score", "progress_level"
        ])

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"
        ordering = ["full_name"]


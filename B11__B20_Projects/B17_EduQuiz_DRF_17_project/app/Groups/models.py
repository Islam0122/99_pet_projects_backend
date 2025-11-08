from django.db import models
from app.User.models import User
from simple_history.models import HistoricalRecords


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
        help_text='Дата и время создания записи.'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления',
        help_text='Дата и время последнего обновления записи.'
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Создатель записи',
        help_text='Пользователь, создавший эту запись.'
    )
    updated_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='updated_%(class)s_set',
        verbose_name='Последний изменивший',
        help_text='Пользователь, последний изменивший эту запись.'
    )

    def save(self, *args, user=None, **kwargs):
        if not self.pk and user:  # Если запись создаётся впервые
            self.created_by = user
            self.updated_user = user
        elif user:  # Если запись уже существует и обновляется
            self.updated_user = user
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Group(BaseModel):
    name = models.CharField(
        max_length=150,
        verbose_name='Название группы',
        help_text='Введите название группы (до 150 символов).'
    )
    history = HistoricalRecords()

    class Meta:
        db_table = 'groups'
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.name


class Student(BaseModel):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='students')
    full_name = models.CharField(
        max_length=150,
        verbose_name='ФИО студента',
        help_text='Введите полное имя студента (до 150 символов).'
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name='Активность студента',
        help_text='Отметьте, если студент активен в системе.'
    )
    history = HistoricalRecords()

    class Meta:
        db_table = 'students'
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

    def __str__(self):
        return self.full_name

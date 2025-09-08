from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    class Meta:
        abstract = True


class Author(BaseModel):
    name = models.CharField(
        max_length=255,
        verbose_name="Имя автора"
    )
    bio = models.TextField(
        blank=True,
        verbose_name="Биография"
    )

    def __str__(self):
        return self.name


class Tag(BaseModel):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Тег"
    )

    def __str__(self):
        return self.name


class Quote(BaseModel):
    text = models.TextField(
        verbose_name="Цитата"
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="quotes",
        verbose_name="Автор"
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="quotes",
        blank=True,
        verbose_name="Теги"
    )

    def __str__(self):
        return f"{self.text[:50]}..."

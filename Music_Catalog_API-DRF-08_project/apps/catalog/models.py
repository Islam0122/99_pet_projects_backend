from django.db import models
import uuid


class Artist(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID исполнителя"
    )
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Имя исполнителя",
        help_text="Введите имя исполнителя (например, Michael Jackson)"
    )
    bio = models.TextField(
        blank=True,
        verbose_name="Биография",
        help_text="Краткая информация об исполнителе"
    )
    country = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Страна",
        help_text="Укажите страну исполнителя"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    class Meta:
        verbose_name = "Исполнитель"
        verbose_name_plural = "Исполнители"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Album(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID альбома"
    )
    title = models.CharField(
        max_length=255,
        verbose_name="Название альбома",
        help_text="Введите название альбома"
    )
    artist = models.ForeignKey(
        Artist,
        related_name="albums",
        on_delete=models.CASCADE,
        verbose_name="Исполнитель",
        help_text="Выберите исполнителя альбома"
    )
    release_year = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Год выпуска",
        help_text="Укажите год выпуска альбома"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание",
        help_text="Краткое описание альбома"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    class Meta:
        verbose_name = "Альбом"
        verbose_name_plural = "Альбомы"
        ordering = ["-release_year", "title"]

    def __str__(self):
        return f"{self.title} ({self.release_year or 'без даты'})"


class Song(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID песни"
    )
    title = models.CharField(
        max_length=255,
        verbose_name="Название песни",
        help_text="Введите название песни"
    )
    duration = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Длительность (сек)",
        help_text="Укажите длительность песни в секундах"
    )
    artist = models.ForeignKey(
        Artist,
        related_name="songs",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Исполнитель",
        help_text="Исполнитель песни (если отличается от альбома)"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    class Meta:
        verbose_name = "Песня"
        verbose_name_plural = "Песни"
        ordering = ["title"]

    def __str__(self):
        return self.title


class AlbumSong(models.Model):
    album = models.ForeignKey(
        Album,
        related_name="album_songs",
        on_delete=models.CASCADE,
        verbose_name="Альбом",
        help_text="Выберите альбом"
    )
    song = models.ForeignKey(
        Song,
        related_name="album_songs",
        on_delete=models.CASCADE,
        verbose_name="Песня",
        help_text="Выберите песню"
    )
    track_number = models.PositiveIntegerField(
        verbose_name="Номер трека",
        help_text="Укажите порядковый номер песни в альбоме"
    )

    class Meta:
        verbose_name = "Трек в альбоме"
        verbose_name_plural = "Треки в альбоме"
        unique_together = (("album", "track_number"), ("album", "song"))
        ordering = ["track_number"]

    def __str__(self):
        return f"{self.track_number}. {self.song.title} ({self.album.title})"

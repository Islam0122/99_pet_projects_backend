from django.apps import AppConfig

class VideoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.Video'
    verbose_name = 'Полезные видео'

    def ready(self):
        import app.Video.signals

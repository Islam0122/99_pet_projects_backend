from django.apps import AppConfig


class TypingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.Typing'
    verbose_name = 'Управления Typing'

    def ready(self):
        import app.Typing.signals

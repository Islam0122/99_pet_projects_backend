from django.apps import AppConfig


class TypingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.words'
    verbose_name = 'Управления Words'

    def ready(self):
        import apps.words.signals

from django.apps import AppConfig


class BroadcastpromptConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.BroadcastPrompt'

    def ready(self):
        import apps.BroadcastPrompt.signals



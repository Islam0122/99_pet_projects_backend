from django.apps import AppConfig


class BroadcastpromptConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.broadcastprompt'

    def ready(self):
        import apps.broadcastprompt.signals



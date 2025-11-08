from django.apps import AppConfig

class GroupsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.Groups'
    verbose_name = 'Группы и студенты'

    def ready(self):
        import app.Groups.signals

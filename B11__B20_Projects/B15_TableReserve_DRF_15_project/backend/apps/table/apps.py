from django.apps import AppConfig


class TableConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.table'

    def ready(self):
        import apps.table.signals

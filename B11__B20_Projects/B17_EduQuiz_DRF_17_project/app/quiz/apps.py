from django.apps import AppConfig


class QuizConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.quiz'
    verbose_name = 'Управления вопросами'

    def ready(self):
        import app.quiz.signals


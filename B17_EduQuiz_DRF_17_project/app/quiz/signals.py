from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.management import call_command
from .models import Question,Topic

@receiver(post_migrate)
def load_initial_data(sender, **kwargs):
    if not Topic.objects.exists():
        call_command('loaddata', 'app/quiz/fixtures/initial_topics_data.json')
    if not Question.objects.exists():
        call_command('loaddata', 'app/quiz/fixtures/initial_questions_data.json')


from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.management import call_command
from .models import Timer , Category , Text

@receiver(post_migrate)
def load_initial_data(sender, **kwargs):
    if not Timer.objects.exists():
        call_command('loaddata', 'apps/words/fixtures/initial_timers_data.json')
    if not Category.objects.exists():
        call_command('loaddata', 'apps/words/fixtures/initial_categories_data.json')
    if not Text.objects.exists():
        call_command('loaddata', 'apps/words/fixtures/initial_texts_data.json')



from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.management import call_command
from .models import Task


@receiver(post_migrate)
def load_task_data(sender, **kwargs):
    if not Task.objects.exists():
        call_command('loaddata', 'apps/tasks/fixtures/initial_tasks.json')

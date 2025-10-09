from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.management import call_command
from .models import Category


@receiver(post_migrate)
def load_category_data(sender, **kwargs):
    if not Category.objects.exists():
        call_command('loaddata', 'apps/tasks/fixtures/initial_category.json')

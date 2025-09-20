from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.management import call_command
from .models import Category


@receiver(post_migrate)
def load_data(sender, **kwargs):
    if not  Category.objects.exists():
        call_command('loaddata', 'apps/category/fixtures/initial_category_data.json')

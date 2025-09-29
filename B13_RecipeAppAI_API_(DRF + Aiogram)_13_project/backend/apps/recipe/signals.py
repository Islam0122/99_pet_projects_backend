from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.management import call_command
from .models import Recipe


@receiver(post_migrate)
def load_data(sender, **kwargs):
    if not  Recipe.objects.exists():
        call_command('loaddata', 'apps/recipe/fixtures/initial_recipe_data.json')

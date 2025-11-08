from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.management import call_command
from .models import Table


@receiver(post_migrate)
def load_data(sender, **kwargs):
    if not  Table.objects.exists():
        call_command('loaddata', 'apps/table/fixtures/initial_data.json')

from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.management import call_command
from .models import Author,Tag,Quote

@receiver(post_migrate)
def load_data(sender, **kwargs):
    if not Author.objects.exists():
        call_command('loaddata', 'apps/quotes/fixtures/initial_Author.json')
    if not Tag.objects.exists():
        call_command('loaddata', 'apps/quotes/fixtures/initial_Tag.json')
    if not Quote.objects.exists():
        call_command('loaddata', 'apps/quotes/fixtures/initial_Quote.json')

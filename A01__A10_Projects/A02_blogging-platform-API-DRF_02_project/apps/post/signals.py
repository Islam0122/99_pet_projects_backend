from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.management import call_command
from .models import Post

@receiver(post_migrate)
def load_post_data(sender, **kwargs):
    if not Post.objects.exists():
        call_command('loaddata', 'apps/post/fixtures/initial_post.json')

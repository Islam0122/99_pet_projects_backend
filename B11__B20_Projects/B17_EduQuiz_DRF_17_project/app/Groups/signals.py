from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.management import call_command
from .models import Group, Student

@receiver(post_migrate)
def load_initial_data(sender, **kwargs):
        if not Group.objects.exists():
            call_command('loaddata', 'app/Groups/fixtures/initial_groups_data.json')
        if not Student.objects.exists():
            call_command('loaddata', 'app/Groups/fixtures/initial_student_data.json')

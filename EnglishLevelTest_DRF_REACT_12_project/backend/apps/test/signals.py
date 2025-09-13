from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.management import call_command
from .models import Test,Level,Question,PlacementTest_Question,PlacementTest


@receiver(post_migrate)
def load_initial_data(sender, **kwargs):
    if not Level.objects.exists():
        call_command('loaddata', 'apps/test/fixtures/initial_level_data.json')
    if not Test.objects.exists():
        call_command('loaddata', 'apps/test/fixtures/initial_test_data.json')
    if not Question.objects.exists():
        call_command('loaddata', 'apps/test/fixtures/initial_quiz_data.json')
    if not PlacementTest.objects.exists():
        call_command('loaddata', 'apps/test/fixtures/initial_placementtest_data.json')
    if not PlacementTest_Question.objects.exists():
        call_command('loaddata', 'apps/test/fixtures/initial_placementtest_question_data.json')


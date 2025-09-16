import os
from celery import Celery

# указываем Django настройки
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# читаем настройки CELERY_* из settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# автоматически подключаем все tasks.py
app.autodiscover_tasks()

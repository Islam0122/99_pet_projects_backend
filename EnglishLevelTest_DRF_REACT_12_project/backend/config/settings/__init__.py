import os
from .celery import app as celery_app

__all__ = ('celery_app',)

ENV = os.getenv('DJANGO_ENV', 'development')

if ENV == 'production':
    from .production import *
elif ENV == 'testing':
    from .testing import *
else:
    from .development import *

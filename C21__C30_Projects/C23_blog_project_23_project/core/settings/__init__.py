import os

ENV = os.getenv('DJANGO_ENV', 'dev')

if ENV == 'prod':
    from .prod import *
elif ENV == 'testing':
    from .testing import *
else:
    from .dev import *

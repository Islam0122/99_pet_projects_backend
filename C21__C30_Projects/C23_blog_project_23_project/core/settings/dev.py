from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler",}},
    "loggers": {
        "django": {"handlers": ["console"], "level": "DEBUG"},
        "blog": {"handlers": ["console"], "level": "DEBUG"},
    },
}

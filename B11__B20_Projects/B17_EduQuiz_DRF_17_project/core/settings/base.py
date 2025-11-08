import os
from datetime import timedelta
from pathlib import Path
from django.utils import timezone
from .env_reader import env
from datetime import timedelta

SECRET_KEY = env('SECRET_KEY')

BASE_DIR = Path(__file__).resolve().parent.parent

PRODUCTION = False

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'django_filters',
    'djoser',
    'corsheaders',
    'drf_yasg',
    'debug_toolbar',
    'simple_history',

    # > apps <
    'app.User',
    'app.Groups',
    'app.quiz',
    'app.Video',
    'app.main',
    'app.Typing',
    'app.Results',
    'app.OTP'
]
# MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Добавьте сюда
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # должен быть до CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]
SIMPLE_HISTORY = {
    'USE_IN_MIGRATIONS': True,
}

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True
STATIC_URL = '/static/'
# URL для статических файлов
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.joinpath("media")

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'User.User'
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=48),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
}

from .cors import *

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "intermetalplus2024@gmail.com"
EMAIL_HOST_PASSWORD = "xlan xouv hbfo zluu"

if not PRODUCTION:
    from .local import *
else:
    from .prod import *

# if DEBUG:
#     INTERNAL_IPS = ['127.0.0.1','localhost',]
#     MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

JAZZMIN_SETTINGS = {
    "site_title": "EduQuiz",  # Заголовок сайта
    "site_header": "Админка EduQuiz",  # Заголовок на главной странице админки
    "site_brand": "EduQuiz",  # Логотип или название бренда на странице
    "welcome_sign": "Добро пожаловать в админку EduQuiz!",  # Приветственное сообщение
    "topmenu_links": [
        {"name": "Главная", "url": "/admin/", "permissions": ["auth.view_user"]},
    ],

    "custom_links": {
        "eduquiz": [
            {"name": "Перейти на сайт", "url": "/", "icon": "fas fa-home", "permissions": []},
        ]
    },
    "show_ui_builder": True,

}
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": True,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-teal",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "litera",
    "dark_mode_theme": "cyborg",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-outline-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}

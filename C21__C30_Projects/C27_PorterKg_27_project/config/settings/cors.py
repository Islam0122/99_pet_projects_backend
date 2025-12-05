CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'accept-language',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^http://127\.0\.0\.1(:\d+)?$",
    r"^http://localhost(:\d+)?$",
    r"^https://islamdev\.up\.railway\.app$",
]
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:63342",
    "http://127.0.0.1:63342",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "https://islamdev.up.railway.app",
]
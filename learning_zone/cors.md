CORS (Cross-Origin Resource Sharing)

# Короткая шпаргалка по CORS — в виде кода/примеров
# Комментарии начинаются с "#". Смотрите примеры для Django, FastAPI, Express.


---

# Что такое CORS
# CORS — механизм браузера, который контролирует, какие домены могут обращаться к вашему серверу.
# Возникает, когда origin (домен/порт/протокол) клиента отличается от origin сервера.


---

# Пример заголовков, которые сервер должен возвращать
HTTP/1.1 200 OK
Access-Control-Allow-Origin: https://example.com
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Allow-Credentials: true
Access-Control-Max-Age: 86400


---

# Django + DRF — пример настройки (settings.py)
INSTALLED_APPS = [
    # ...
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    # ...
]

# Разрешить все домены (только для разработки)
CORS_ALLOW_ALL_ORIGINS = True

# Или явный список доменов
CORS_ALLOWED_ORIGINS = [
    'https://example.com',
    'https://app.example.com',
]

# Разрешить cookies
CORS_ALLOW_CREDENTIALS = True


---

# FastAPI — минимальный пример
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.get('/')
async def root():
    return {'ok': True}


---

// Express (Node.js)
const express = require('express')
const cors = require('cors')
const app = express()

// Простая настройка — разрешить все (dev)
app.use(cors())

// Или с опциями
app.use(cors({
  origin: ['https://example.com', 'https://app.example.com'],
  credentials: true,
  methods: ['GET','POST','PUT','DELETE','OPTIONS'],
}))

app.get('/', (req, res) => res.json({ok: true}))


---

# Preflight (OPTIONS)
# Браузер отправляет OPTIONS перед основным запросом, если запрос не "простой".
# Сервер должен вернуть 200 и соответствующие Access-Control-* заголовки.

OPTIONS /api/resource HTTP/1.1
Origin: https://app.example.com
Access-Control-Request-Method: PUT
Access-Control-Request-Headers: X-Custom-Header

# Ответ от сервера:
HTTP/1.1 204 No Content
Access-Control-Allow-Origin: https://app.example.com
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: X-Custom-Header, Authorization
Access-Control-Max-Age: 3600


---

# Лучшие практики (в виде списка):
# 1) В prod указывайте конкретные домены, не ставьте '*'.
# 2) Включайте credentials только если реально нужны cookies/авторизация.
# 3) Ограничивайте методы и заголовки.
# 4) Настройте кеширование preflight (Access-Control-Max-Age).
# 5) Тестируйте с техдомена, который будет у продакшена (https + точный порт).


---

# Полезные команды для проверки
# 1) curl (простой запрос)
curl -i -H "Origin: https://app.example.com" https://api.example.com/resource

# 2) Пример preflight с curl
curl -i -X OPTIONS \
  -H "Origin: https://app.example.com" \
  -H "Access-Control-Request-Method: PUT" \
  -H "Access-Control-Request-Headers: X-Custom-Header" \
  https://api.example.com/resource


---

# Заключение
# Этот файл теперь оформлен в виде кода и примеров. Если хочешь — могу:
# - добавить конкретный пример для твоего бэкенда (Django/FastAPI/Express),
# - сделать краткую версию на английском,
# - или оформить как README.md для репозитория.
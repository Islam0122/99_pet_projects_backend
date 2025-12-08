# CORS (Cross-Origin Resource Sharing)

## 📌 Что такое CORS?

**CORS** — это механизм безопасности браузера, который контролирует, какие домены могут обращаться к ресурсам вашего API.

**Origin** = протокол + домен + порт

```
https://example.com:443  ← Origin
│      │           │
│      │           └─ порт
│      └───────────── домен
└──────────────────── протокол
```

---

## 🔑 Основные HTTP-заголовки

| Заголовок | Описание | Пример |
|-----------|----------|--------|
| `Access-Control-Allow-Origin` | Разрешенные домены | `https://app.example.com` или `*` |
| `Access-Control-Allow-Methods` | Разрешенные HTTP-методы | `GET, POST, PUT, DELETE` |
| `Access-Control-Allow-Headers` | Разрешенные заголовки | `Content-Type, Authorization` |
| `Access-Control-Allow-Credentials` | Разрешить cookies/авторизацию | `true` |
| `Access-Control-Max-Age` | Кеширование preflight (секунды) | `86400` (24 часа) |
| `Access-Control-Expose-Headers` | Какие заголовки доступны клиенту | `X-Custom-Header` |

---

## 🎯 Типы запросов

### Простой запрос (Simple Request)
Не требует preflight, если:
- Метод: `GET`, `HEAD`, `POST`
- Заголовки: только `Accept`, `Content-Type`, `Content-Language`
- `Content-Type`: только `application/x-www-form-urlencoded`, `multipart/form-data`, `text/plain`

### Preflight запрос (OPTIONS)
Браузер отправляет **OPTIONS** перед основным запросом, если:
- Используются методы `PUT`, `DELETE`, `PATCH`
- Кастомные заголовки (например, `Authorization`)
- `Content-Type`: `application/json`

```http
OPTIONS /api/users HTTP/1.1
Origin: https://app.example.com
Access-Control-Request-Method: PUT
Access-Control-Request-Headers: Authorization, Content-Type
```

**Ответ сервера:**
```http
HTTP/1.1 204 No Content
Access-Control-Allow-Origin: https://app.example.com
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Authorization, Content-Type
Access-Control-Max-Age: 3600
```

---

## 💻 Примеры настройки

### Django + django-cors-headers

**1. Установка:**
```bash
pip install django-cors-headers
```

**2. Настройка `settings.py`:**
```python
INSTALLED_APPS = [
    # ...
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # ...
]

# Для разработки (разрешить все)
CORS_ALLOW_ALL_ORIGINS = True

# Для production (конкретные домены)
CORS_ALLOWED_ORIGINS = [
    'https://example.com',
    'https://app.example.com',
    'http://localhost:3000',  # для локальной разработки
]

# Разрешить cookies/авторизацию
CORS_ALLOW_CREDENTIALS = True

# Дополнительные настройки
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
    'authorization',
    'content-type',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Кеширование preflight
CORS_PREFLIGHT_MAX_AGE = 86400  # 24 часа
```

---

### FastAPI

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Список разрешенных доменов
origins = [
    "https://example.com",
    "https://app.example.com",
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # или ["*"] для разработки
    allow_credentials=True,
    allow_methods=["*"],    # или конкретные: ["GET", "POST"]
    allow_headers=["*"],    # или конкретные заголовки
    max_age=3600,          # кеширование preflight
)

@app.get("/api/users")
async def get_users():
    return {"users": ["Alice", "Bob"]}

@app.post("/api/users")
async def create_user(name: str):
    return {"user": name, "created": True}
```

### Flask

**1. Установка:**
```bash
pip install flask-cors
```

**2. Настройка:**
```python
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

# Простая настройка
CORS(app)

# Или с параметрами
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://example.com", "http://localhost:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True,
        "max_age": 3600
    }
})

@app.route('/api/users')
def get_users():
    return {'users': ['Alice', 'Bob']}
```

---

## ⚠️ Частые ошибки и решения

| Ошибка | Причина | Решение |
|--------|---------|---------|
| `No 'Access-Control-Allow-Origin' header` | Сервер не возвращает CORS-заголовки | Добавить middleware/настройки CORS |
| `Credentials flag is true, but Access-Control-Allow-Origin is '*'` | Нельзя использовать `*` с credentials | Указать конкретный домен |
| `Method not allowed` | Метод не указан в `Allow-Methods` | Добавить метод в настройки |
| `Header not allowed` | Заголовок не указан в `Allow-Headers` | Добавить заголовок в настройки |
| Preflight запрос возвращает 404/500 | OPTIONS не обрабатывается | Проверить маршрутизацию OPTIONS |

---

## 🔍 Отладка CORS

### 1. Проверка с curl

**Простой запрос:**
```bash
curl -i -H "Origin: https://app.example.com" \
  https://api.example.com/users
```

**Preflight запрос:**
```bash
curl -i -X OPTIONS \
  -H "Origin: https://app.example.com" \
  -H "Access-Control-Request-Method: PUT" \
  -H "Access-Control-Request-Headers: Content-Type, Authorization" \
  https://api.example.com/users
```

### 2. Проверка в браузере (DevTools)

```javascript
// Откройте консоль браузера на https://app.example.com
fetch('https://api.example.com/users', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer token'
  },
  credentials: 'include',
  body: JSON.stringify({ name: 'Alice' })
})
.then(r => r.json())
.then(console.log)
.catch(console.error);
```

Откройте вкладку **Network** → найдите запрос → вкладка **Headers** → проверьте `Response Headers`.

---

## ✅ Лучшие практики

| Практика | Разработка | Production |
|----------|-----------|-----------|
| `Allow-Origin` | `*` или `localhost` | Конкретные домены |
| `Allow-Credentials` | `true` (если нужно) | `true` (только если необходимо) |
| `Allow-Methods` | `*` | Только необходимые методы |
| `Allow-Headers` | `*` | Только необходимые заголовки |
| `Max-Age` | `600` (10 мин) | `86400` (24 часа) |

### 🔒 Безопасность

```python
# ❌ Небезопасно для production
CORS_ALLOW_ALL_ORIGINS = True

# ✅ Безопасно
CORS_ALLOWED_ORIGINS = [
    'https://example.com',
    'https://app.example.com',
]

# ❌ Избегайте
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true  # Этот комбинация невозможна

# ✅ Правильно
Access-Control-Allow-Origin: https://app.example.com
Access-Control-Allow-Credentials: true
```

---

## 📋 Чек-лист для деплоя

- [ ] Указаны конкретные домены (не `*`)
- [ ] `credentials: true` только если нужны cookies
- [ ] Ограничены методы и заголовки
- [ ] Настроен `Max-Age` для кеширования preflight
- [ ] Протестировано с реального домена (не `localhost`)
- [ ] HTTPS включен для production
- [ ] CORS middleware установлен первым в цепочке
- [ ] OPTIONS запросы возвращают 200/204

---

## 🔗 Полезные ссылки

- [MDN: Cross-Origin Resource Sharing](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [django-cors-headers docs](https://github.com/adamchainz/django-cors-headers)
- [FastAPI CORS middleware](https://fastapi.tiangolo.com/tutorial/cors/)

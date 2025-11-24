CORS (Cross-Origin Resource Sharing)

Что такое CORS

CORS — это механизм безопасности браузеров, который контролирует, какие домены могут отправлять запросы к серверу. Он нужен для защиты пользователя от вредоносных сайтов, которые пытаются обращаться к API без разрешения.

Где используется

В веб‑приложениях

В REST API

В SPA (React, Vue)

В мобильных приложениях, которые общаются с сервером


Почему возникает ошибка CORS

Ошибка появляется, когда браузер блокирует запрос, потому что:

домен клиента и сервера разные;

сервер не указал необходимые заголовки CORS;

используются методы или заголовки, требующие preflight‑запроса (OPTIONS).


Ключевые заголовки CORS

Access-Control-Allow-Origin — разрешённый источник (домен).

Access-Control-Allow-Methods — разрешённые HTTP‑методы.

Access-Control-Allow-Headers — разрешённые заголовки.

Access-Control-Allow-Credentials — можно ли передавать cookies.

Access-Control-Max-Age — время кеширования preflight.


Простые запросы

Запрос считается простым, если:

метод: GET, POST, HEAD;

заголовки только Accept, Content-Type, Content-Language и др. стандартные;

Content-Type один из: application/x-www-form-urlencoded, multipart/form-data, text/plain.


Простые запросы не вызывают preflight (OPTIONS).

Preflight (OPTIONS) запрос

Браузер отправляет OPTIONS, чтобы сервер подтвердил разрешения, если:

используются методы: PUT, PATCH, DELETE;

есть кастомные заголовки;

тип content-type — нестандартный.


Как разрешить CORS в разных фреймворках

Django + DRF

Установить:

pip install django-cors-headers

Добавить в settings.py:

INSTALLED_APPS = [
    ...,
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...,
]

CORS_ALLOW_ALL_ORIGINS = True  # или жестко прописать домены

FastAPI

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Node.js (Express)

npm install cors

const cors = require('cors')
app.use(cors())

Лучшие практики

Не ставить * в продакшене — указывать домены.

Включать credentials (cookies) только при необходимости.

Лимитировать методы и заголовки.

Кешировать preflight запросы.


Итого

CORS — это важная часть безопасности, которая предотвращает несанкционированный доступ к вашему API. Чтобы избежать ошибок, нужно правильно настроить заголовки и понимать, как браузер делает запросы.
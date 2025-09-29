# Music Catalog API

REST API для каталога исполнителей, альбомов и песен. 
Позволяет создавать, читать, обновлять и удалять исполнителей,
альбомы и песни, а также управлять их связями. Подключена документация Swagger для ручного тестирования.
---

## 📦 Структура проекта

```

apps/
└── catalog/      # Приложение с моделями, сериализаторами и viewsets
config/           # Django конфигурации (settings, urls)
Dockerfile
docker-compose.yml
manage.py
requirements.txt
README.md

````

## 📝 API Endpoints

| Сущность      | Endpoint                  | Методы                  |
| ------------- | ------------------------- | ----------------------- |
| Исполнители   | `/api/artists/`           | GET, POST               |
| Исполнитель   | `/api/artists/{id}/`      | GET, PUT, PATCH, DELETE |
| Альбомы       | `/api/albums/`            | GET, POST               |
| Альбом        | `/api/albums/{id}/`       | GET, PUT, PATCH, DELETE |
| Песни альбома | `/api/albums/{id}/songs/` | GET, POST               |
| Песни         | `/api/songs/`             | GET, POST               |
| Песня         | `/api/songs/{id}/`        | GET, PUT, PATCH, DELETE |


* В проекте тесты покрывают \~97% кода.


## 📝 Используемые технологии

* Python 3.13
* Django 4.x
* Django REST Framework
* drf-spectacular (Swagger / OpenAPI)
* PostgreSQL (через Docker)
* Docker & docker-compose

---

## ✅ Чек-лист готовности к сдаче

* [x] CRUD для Artist / Album / Song
* [x] Связь песен и альбомов с `track_number`
* [x] Swagger документация доступна
* [x] Тесты покрывают основные модели и viewsets
* [x] Docker + docker-compose для быстрого запуска
* [x] README с инструкцией запуска и API

---


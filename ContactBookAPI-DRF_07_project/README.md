# ContactBookAPI-DRF

Простой API для хранения контактов с авторизацией через JWT. Проект написан на Django + DRF.

---

## 📦 Структура проекта

- `apps/user/` — регистрация, логин, JWT.
- `apps/contactbook/` — CRUD контактов.
- `config/` — настройки проекта.
- `Dockerfile` и `docker-compose.yml` — запуск через Docker.


## 🔑 Endpoints

### Пользователи

* `POST /register/` — регистрация
* `POST /login/` — получение JWT
* `POST /logout/` — выход
* `POST /token/refresh/` — обновление токена
* `GET /protected/` — защищённый endpoint (только для авторизованных)

### Контакты

* `GET /api/contacts/` — список контактов пользователя
* `POST /api/contacts/` — создать контакт
* `GET /api/contacts/<id>/` — получить контакт
* `PUT /api/contacts/<id>/` — обновить контакт
* `DELETE /api/contacts/<id>/` — удалить контакт

---

## 🧪 Тесты

```bash
python manage.py test
coverage run manage.py test
coverage report -m
```

---

## ⚙️ Особенности
* JWT авторизация
* Фильтрация контактов по пользователю
* Поддержка email, телефона, адреса, тегов
* Docker-ready


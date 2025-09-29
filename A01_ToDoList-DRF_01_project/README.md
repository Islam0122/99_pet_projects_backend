
# ToDoList API (Django)

## 📌 О проекте
**ToDoList** — это API для управления задачами (CRUD): create, get, get_list, update, delete.  
Модель задачи содержит: `uuid`, `title`, `description`, `status` (created, in_progress, completed).  

Проект написан на Django с использованием Django Rest Framework (DRF), легко масштабируется и расширяется.


---

## 🛠 Используемые технологии

- **Python 3.10+**
- **Django 5.x**
- **Django Rest Framework (DRF)**
- **PostgreSQL / SQLite** (по умолчанию SQLite)
- **django-environ** — работа с `.env`
- **django-cors-headers** — поддержка CORS
- **drf-yasg** — Swagger / OpenAPI документация
- **jazzmin** — кастомизация админки
- **Docker & Docker Compose**
- **Git** — контроль версий
- **pytest & pytest-django** — тесты

---

## ⚙️ Настройка проекта локально

1. Клонируем репозиторий:

```bash
git clone <URL>
cd <project_folder>
````

2. Создаём виртуальное окружение:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Создаём файл `.env` в корне проекта:

```bash
touch .env
```

Содержимое `.env`:

```env
# Общие настройки
DEBUG=True
DJANGO_ENV=development
SECRET_KEY=django-insecure-*2_bor@=uq@qt1o@

# Разрешённые хосты
ALLOWED_HOSTS=127.0.0.1,localhost

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000

# База данных (для SQLite не обязательно)
DATABASE_URL=sqlite:///db.sqlite3
# Для PostgreSQL:
# DATABASE_URL=postgres://user:password@db:5432/dbname

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=intermetalplus2024@gmail.com
EMAIL_HOST_PASSWORD=секретный_пароль
```

4. Устанавливаем зависимости:

```bash
pip install -r requirements.txt
```

5. Применяем миграции и загружаем фикстуры:

```bash
python manage.py migrate
python manage.py loaddata apps/tasks/fixtures/initial_tasks.json
```

6. Запуск сервера:

```bash
python manage.py runserver
```

Swagger документация: [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)

Пример запроса через curl:

```bash
curl http://127.0.0.1:8000/api/tasks/
```

---

## 🐳 Запуск через Docker

1. Собираем контейнер и запускаем:

```bash
docker-compose up --build
```

* Сервер будет доступен на `http://localhost:8000`.
* Миграции и fixtures применяются автоматически.

2. Для пересборки без кеша:

```bash
docker-compose build --no-cache
docker-compose up
```

3. Для остановки:

```bash
docker-compose down
```

---

## 🧪 Тесты

Запуск тестов локально:

```bash
pytest -v
```

Запуск тестов через Docker (если настроен отдельный сервис `tests`):

```bash
docker-compose run tests
```

* Покрытие CRUD полностью тестируется, включая create, get, update и delete.

---

## 📂 Структура проекта

```
.
├── apps/tasks/        # приложение с моделью Task, views, serializers, tests, fixtures
├── config/settings/   # настройки проекта (development, production, testing)
├── Dockerfile
├── docker-compose.yml
├── README.md
├── manage.py
├── requirements.txt
```



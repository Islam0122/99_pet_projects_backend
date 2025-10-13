# 📝 ToDoList Telegram Bot

Проект представляет собой Telegram-бота для управления задачами с уведомлениями через Celery и интеграцией с Django REST API.

Используемые технологии:

* **Backend:** Django + Django REST Framework (DRF)
* **Telegram Bot:** Aiogram + Aiogram-Dialog
* **Асинхронные задачи:** Celery + Redis
* **База данных:** PostgreSQL
* **Docker:** Контейнеризация всех сервисов

---

## ⚡ Функционал

* Создание и управление задачами через Telegram и REST API
* Категории задач (теги)
* Уведомления через Telegram:

  * Созданная задача
  * Дедлайн задачи
  * Незавершённые задачи
* Статистика пользователя:

  * Количество выполненных задач
  * Серия дней подряд с выполнением задач
* Интерактивные диалоги для добавления задач через Aiogram-Dialog

---

## 🏗 Архитектура

```
Telegram Bot <--> DRF API <--> PostgreSQL
         |             |
         |             v
         |          Celery <--> Redis (Брокер)
         |             |
         v             v
    Aiogram-Dialog  Фоновая обработка задач
```

### Docker сервисы

| Сервис          | Назначение                                                                 |
| --------------- | -------------------------------------------------------------------------- |
| `web`           | Django + DRF API — основной backend и REST API. Выполняет миграции и запускает сервер на `0.0.0.0:8000`. |
| `bot`           | Telegram Bot — взаимодействует с пользователями через Aiogram + Aiogram-Dialog. |
| `celery_worker` | Фоновая обработка задач через Celery (отправка уведомлений, задачи с дедлайнами). |
| `celery_beat`   | Планировщик периодических задач Celery Beat (регулярная отправка напоминаний). |
| `redis`         | Брокер сообщений для Celery (хранит очередь задач).                        |
| `db`            | PostgreSQL база данных для хранения пользователей, задач и категорий.     |

---

## 🗄 Структура базы данных

```
┌──────────┐       ┌────────────┐       ┌───────────┐
│  TGUser  │      *│   Task     │*     *│ Category  │
├──────────┤       ├────────────┤       ├───────────┤
│ id       │◄──────│ owner_id   │       │ id        │
│ telegram_id │     │ title     │       │ name      │
│ username │       │ description│       │ created_at│
│ streak_days│      │ due_date  │       └───────────┘
│ last_task_completed│ done     │
└──────────┘       │ created_reminder_sent │
                   │ due_reminder_sent    │
                   └────────────┘
```

### **TGUser**

Хранит данные пользователей Telegram.

| Поле                   | Тип           | Описание                             |
| ---------------------- | ------------- | ------------------------------------ |
| `telegram_id`          | CharField     | Уникальный ID пользователя           |
| `username`             | CharField     | Имя пользователя (необязательно)     |
| `created_at`           | DateTimeField | Дата создания                        |
| `total_task_completes` | IntegerField  | Кол-во выполненных задач             |
| `streak_days`          | IntegerField  | Серия дней подряд                    |
| `last_task_completed`  | DateTimeField | Дата последнего выполненного задания |

Методы:

* `update_streak()` — обновляет серию дней подряд.

---

### **Category**

Категории (теги) для задач.

| Поле         | Тип           | Описание                       |
| ------------ | ------------- | ------------------------------ |
| `id`         | SnowflakePK   | Уникальный ID категории        |
| `name`       | CharField     | Название категории, уникальное |
| `created_at` | DateTimeField | Дата создания категории        |

Связи:

* `tasks` — ManyToMany с моделью **Task**

---

### **Task**

Модель задачи.

| Поле                    | Тип                   | Описание                          |
| ----------------------- | --------------------- | --------------------------------- |
| `id`                    | SnowflakePK           | Уникальный ID задачи              |
| `title`                 | CharField             | Название задачи                   |
| `description`           | TextField             | Описание задачи                   |
| `owner`                 | ForeignKey → TGUser   | Владелец задачи                   |
| `categories`            | ManyToMany → Category | Категории задачи                  |
| `created_at`            | DateTimeField         | Дата создания                     |
| `due_date`              | DateTimeField         | Дедлайн задачи                    |
| `done`                  | BooleanField          | Выполнена или нет                 |
| `created_reminder_sent` | BooleanField          | Напоминание о создании отправлено |
| `due_reminder_sent`     | BooleanField          | Напоминание о дедлайне отправлено |

---

## 📝 Celery задачи и уведомления

1. **send_task_reminders**

   * Уведомление о создании задачи
   * Напоминание о приближающемся дедлайне

2. **remind_unfinished_tasks**

   * Регулярное напоминание о незавершённых задачах

Celery Beat Schedule пример:

```python
CELERY_BEAT_SCHEDULE = {
    "send-task-reminders-every-5-min": {
        "task": "apps.tasks.tasks.send_task_reminders",
        "schedule": 300.0,
    },
    "remind-unfinished-tasks-every-10-min": {
        "task": "apps.tasks.tasks.remind_unfinished_tasks",
        "schedule": 600.0,
    },
}
```

---

## 🐳 Docker & запуск проекта

### 1. Сборка контейнеров

```bash
docker-compose build
```

### 2. Запуск контейнеров

```bash
docker-compose up -d
```

### 3. Миграции базы данных

```bash
docker-compose exec web python manage.py migrate
```

### 4. Создание суперпользователя

```bash
docker-compose exec web python manage.py createsuperuser
```

### 5. Просмотр логов

```bash
docker-compose logs -f
```

---

## 🔧 Настройки через `.env`

```env
SECRET_KEY=
DEBUG=True
DJANGO_ENV=development
TELEGRAM_BOT_TOKEN=
TELEGRAM_API_URL=http://web:8000/api/v1
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=5432
```




# 📘 SQLite3

## 📌 Что такое SQLite?

SQLite — это встроенная (embedded) реляционная база данных, которая хранится в одном файле.

Не требует сервера, проста в установке, идеальна для небольших и средних проектов.

---

## 📂 Где используется?

- мобильные приложения (Android, iOS)
- настольные программы
- небольшие веб-проекты
- боты
- локальные инструменты и утилиты

---

## 🧱 Основные особенности

- База хранится в одном `.db` файле
- Очень быстрая
- ACID-совместимая
- Поддерживает SQL-запросы
- Нет отдельного сервера → проще деплой
- Ограничена для больших нагрузок

---

## ⚙️ Основные команды SQL в SQLite

### Создание таблицы

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

### Добавление данных

```sql
INSERT INTO users (name, age) VALUES ('Islam', 18);
```

### Получение данных

```sql
SELECT * FROM users;
SELECT name, age FROM users WHERE age > 18;
```

### Обновление данных

```sql
UPDATE users SET age = 19 WHERE id = 1;
```

### Удаление данных

```sql
DELETE FROM users WHERE id = 1;
```

---

## 🔌 Использование SQLite3 в Python

### Подключение

```python
import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()
```

### Создание таблицы

```python
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER
)
""")
conn.commit()
```

### Добавление данных

```python
cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Islam", 18))
conn.commit()
```

### Получение данных

```python
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
for row in rows:
    print(row)
```

### Закрытие соединения

```python
conn.close()
```

---

## 🔍 Полезные фишки

### Проверить структуру таблицы

```sql
PRAGMA table_info(users);
```

### Список всех таблиц

```sql
SELECT name FROM sqlite_master WHERE type='table';
```

### Индексы

```sql
CREATE INDEX idx_users_name ON users(name);
```

---

## 📦 Плюсы и минусы

### ✔️ Плюсы

- очень лёгкая
- одна база = один файл
- не требует сервера
- простая интеграция с Python
- быстрые операции

### ❌ Минусы

- не подходит для больших нагрузок
- нет доступа по сети
- нет сложной системы прав

---

## 🐍 SQLite в Django

### Подключение в `settings.py`

SQLite подключена по умолчанию в Django:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # путь к файлу базы данных
    }
}
```

### Создание моделей

```python
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
```

### Миграции

```bash
python manage.py makemigrations
python manage.py migrate
```

### Работа с данными

```python
# Создание
user = User.objects.create(name="Islam", age=18)

# Получение всех
users = User.objects.all()

# Фильтрация
adult_users = User.objects.filter(age__gte=18)

# Получение одного
user = User.objects.get(id=1)

# Обновление
user.age = 19
user.save()

# Удаление
user.delete()
```

### Django Shell

```bash
python manage.py shell
```

```python
from myapp.models import User

# Работайте с данными напрямую
User.objects.create(name="Test", age=25)
```

---

## ⚡ SQLite в FastAPI

### Установка зависимостей

```bash
pip install fastapi sqlalchemy aiosqlite
```

### Подключение базы данных (`database.py`)

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Создание модели (`models.py`)

```python
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
```

### Схемы Pydantic (`schemas.py`)

```python
from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    age: int

class UserResponse(BaseModel):
    id: int
    name: str
    age: int
    created_at: datetime

    class Config:
        from_attributes = True
```

### API endpoints (`main.py`)

```python
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Создать пользователя
@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(name=user.name, age=user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Получить всех пользователей
@app.get("/users/", response_model=List[schemas.UserResponse])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

# Получить одного пользователя
@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Обновить пользователя
@app.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_user.name = user.name
    db_user.age = user.age
    db.commit()
    db.refresh(db_user)
    return db_user

# Удалить пользователя
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}
```

### Запуск FastAPI

```bash
uvicorn main:app --reload
```

Документация доступна по адресу: `http://localhost:8000/docs`

---

## 🔄 Сравнение Django vs FastAPI

| Особенность | Django | FastAPI |
|------------|--------|---------|
| **ORM** | Встроенный Django ORM | SQLAlchemy |
| **Миграции** | Автоматические | Alembic (опционально) |
| **Скорость** | Средняя | Очень быстрая |
| **Async** | Частично | Полная поддержка |
| **Документация API** | DRF (опционально) | Автоматическая (Swagger) |
| **Простота** | Проще для начинающих | Более гибкая |

---

## 💡 Советы по использованию

### Django
- Используйте `select_related()` и `prefetch_related()` для оптимизации запросов
- Включите Django Debug Toolbar для анализа запросов
- Используйте индексы для часто запрашиваемых полей

### FastAPI
- Используйте async/await для асинхронных операций
- Добавьте Alembic для управления миграциями
- Используйте dependency injection для переиспользования кода
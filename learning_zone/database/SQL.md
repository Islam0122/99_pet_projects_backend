# SQL + Python — Шпаргалка

## 🔹 SELECT — Выборка
```sql
SELECT * FROM users;
SELECT name, email FROM users WHERE age > 18;
SELECT * FROM users ORDER BY id DESC LIMIT 10;
```

## 🔹 INSERT — Добавление
```sql
INSERT INTO users (name, email, age) 
VALUES ('Islam', 'test@mail.com', 16);
```

## 🔹 UPDATE — Обновление
```sql
UPDATE users SET age = 17 WHERE id = 1;
```

## 🔹 DELETE — Удаление
```sql
DELETE FROM users WHERE id = 4;
```

## 🔹 CREATE TABLE — Создание таблицы
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    age INT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## 🔹 JOIN — Связь таблиц
```sql
SELECT users.name, orders.amount
FROM users
JOIN orders ON users.id = orders.user_id;
```

## 🔹 GROUP BY — Группировка
```sql
SELECT status, COUNT(*) FROM orders GROUP BY status;
```

---

## 🐍 Python + SQLite

```python
import sqlite3

conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()

# Создать таблицу
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER
)
""")

# Добавить данные
cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Islam", 16))

# Выборка
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Обновить
cursor.execute("UPDATE users SET age = ? WHERE id = ?", (17, 1))

# Удалить
cursor.execute("DELETE FROM users WHERE id = ?", (1,))

conn.commit()
conn.close()
```

---

## 🐘 Python + PostgreSQL

```python
import psycopg2

conn = psycopg2.connect(
    dbname="db",
    user="postgres",
    password="12345",
    host="localhost"
)
cursor = conn.cursor()

cursor.execute("SELECT * FROM users")
print(cursor.fetchall())

conn.close()
```

---

## ⚡ Полезные команды

```sql
-- Уникальные значения
SELECT DISTINCT country FROM users;

-- Подсчёт
SELECT COUNT(*) FROM users;

-- Агрегация
SELECT AVG(price), SUM(price), MAX(price) FROM products;

-- Очистка таблицы
TRUNCATE TABLE users RESTART IDENTITY;
```
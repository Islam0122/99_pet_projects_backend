
# MySQL — краткий конспект

## 1. Что такое MySQL

**MySQL** — это реляционная система управления базами данных (СУБД), работающая с SQL (Structured Query Language).

Используется для:

* сайтов и веб‑приложений
* хранения пользователей, заказов, сообщений и т.д.
* бэкенда (Django, FastAPI, PHP, Node.js)

---

## 2. Основные понятия

* **База данных (Database)** — контейнер для таблиц
* **Таблица (Table)** — хранит данные в виде строк и столбцов
* **Строка (Row)** — одна запись
* **Столбец (Column)** — одно поле (id, name, email)
* **Первичный ключ (PRIMARY KEY)** — уникальный идентификатор
* **Внешний ключ (FOREIGN KEY)** — связь между таблицами

---

## 3. Подключение к MySQL

```bash
mysql -u root -p
```

или

```bash
mysql -u user -p db_name
```

---

## 4. Работа с базами данных

### Создать базу данных

```sql
CREATE DATABASE test_db;
```

### Посмотреть базы данных

```sql
SHOW DATABASES;
```

### Выбрать базу данных

```sql
USE test_db;
```

### Удалить базу данных

```sql
DROP DATABASE test_db;
```

---

## 5. Работа с таблицами

### Создание таблицы

```sql
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(100),
  age INT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Показать таблицы

```sql
SHOW TABLES;
```

### Структура таблицы

```sql
DESCRIBE users;
```

### Удалить таблицу

```sql
DROP TABLE users;
```

---

## 6. CRUD операции

### INSERT — добавление данных

```sql
INSERT INTO users (name, email, age)
VALUES ('Ali', 'ali@mail.com', 20);
```

### SELECT — получение данных

```sql
SELECT * FROM users;
SELECT name, age FROM users;
```

### WHERE — фильтрация

```sql
SELECT * FROM users WHERE age > 18;
```

### UPDATE — обновление

```sql
UPDATE users SET age = 21 WHERE id = 1;
```

### DELETE — удаление

```sql
DELETE FROM users WHERE id = 1;
```

---

## 7. Сортировка и лимиты

```sql
SELECT * FROM users ORDER BY age DESC;
SELECT * FROM users LIMIT 5;
```

---

## 8. Агрегатные функции

```sql
SELECT COUNT(*) FROM users;
SELECT AVG(age) FROM users;
SELECT MAX(age), MIN(age) FROM users;
```

---

## 9. Связи между таблицами

### Пример

```sql
CREATE TABLE orders (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT,
  total DECIMAL(10,2),
  FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### JOIN

```sql
SELECT users.name, orders.total
FROM users
JOIN orders ON users.id = orders.user_id;
```

---

## 10. Индексы

```sql
CREATE INDEX idx_email ON users(email);
```

Ускоряют поиск

---

## 11. Пользователи и права

```sql
CREATE USER 'dev'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON test_db.* TO 'dev'@'localhost';
FLUSH PRIVILEGES;
```

---

## 12. MySQL + Python (пример)

```python
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="test_db"
)

cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
print(cursor.fetchall())
```

---

## 13. Полезные команды

```sql
SELECT VERSION();
SHOW PROCESSLIST;
EXIT;
```


* GitHub
* Obsidian / Notion

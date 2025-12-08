# 📘 Makefile - Полное руководство для разработчика

## 🎯 Что такое Makefile?

**Makefile** — это файл с набором инструкций (правил) для утилиты `make`, которая автоматизирует рутинные задачи в разработке. Изначально создан для компиляции C/C++ программ, но широко используется в любых проектах для автоматизации.

### Зачем нужен Makefile в Django проекте?

✅ **Автоматизация** — одна команда вместо цепочки из 5-10 команд  
✅ **Документация** — новый разработчик видит все доступные команды через `make help`  
✅ **Стандартизация** — все в команде используют одинаковые команды  
✅ **Экономия времени** — не нужно помнить длинные команды Django  
✅ **Безопасность** — меньше опечаток в критических командах  

---

## 📋 Базовый синтаксис Makefile

### Структура правила (target)

```makefile
target: dependencies
	command1
	command2
```

**Важно!** Перед командами должна быть **табуляция (TAB)**, а не пробелы.

### Пример простого Makefile

```makefile
# Комментарий начинается с #

# Правило без зависимостей
hello:
	echo "Hello, World!"

# Правило с зависимостью
build: install
	python manage.py migrate

install:
	pip install -r requirements.txt
```

**Использование:**
```bash
make hello    # Выполнит: echo "Hello, World!"
make build    # Сначала выполнит install, потом migrate
```

---

## 🔧 Makefile для Django проекта (из вашего задания)

Разберем построчно реальный Makefile:

```makefile
.PHONY: help install migrate run test clean docker-build docker-up docker-down

help:
	@echo "Доступные команды:"
	@echo "  make install       - Установка зависимостей"
	@echo "  make migrate       - Выполнение миграций"
	@echo "  make fixtures      - Загрузка тестовых данных"
	@echo "  make users         - Создание тестовых пользователей"
	@echo "  make run           - Запуск development сервера"
	@echo "  make test          - Запуск тестов"
	@echo "  make clean         - Очистка временных файлов"
	@echo "  make docker-build  - Сборка Docker образа"
	@echo "  make docker-up     - Запуск в Docker"
	@echo "  make docker-down   - Остановка Docker контейнеров"

install:
	pip install -r requirements.txt

migrate:
	python manage.py makemigrations
	python manage.py migrate

fixtures:
	python manage.py loaddata fixtures/initial_data.json

users:
	python manage.py create_test_users

setup: install migrate fixtures users
	python manage.py collectstatic --noinput
	@echo "✅ Проект настроен!"

run:
	python manage.py runserver

test:
	pytest

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d
	docker-compose exec web python manage.py migrate
	docker-compose exec web python manage.py loaddata fixtures/initial_data.json
	docker-compose exec web python manage.py create_test_users

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

superuser:
	python manage.py createsuperuser

shell:
	python manage.py shell
```

---

## 📖 Подробный разбор команд

### 1. `.PHONY` — фиктивные цели

```makefile
.PHONY: help install migrate run
```

**Назначение:** Указывает, что это не реальные файлы, а команды.

**Зачем нужно:**
- Если в проекте есть файл с именем `test`, то `make test` попытается проверить файл, а не выполнить команду
- `.PHONY` заставляет make всегда выполнять команду, даже если файл существует

---

### 2. `help` — справка по командам

```makefile
help:
	@echo "Доступные команды:"
	@echo "  make install - Установка зависимостей"
```

**Символ `@`** — подавляет вывод самой команды (показывает только результат).

**Без `@`:**
```
echo "Доступные команды:"
Доступные команды:
```

**С `@`:**
```
Доступные команды:
```

---

### 3. `install` — установка зависимостей

```makefile
install:
	pip install -r requirements.txt
```

**Использование:**
```bash
make install
```

**Эквивалент:**
```bash
pip install -r requirements.txt
```

---

### 4. `migrate` — миграции БД

```makefile
migrate:
	python manage.py makemigrations
	python manage.py migrate
```

**Выполнит последовательно:**
1. Создаст новые миграции
2. Применит их к базе данных

**Использование:**
```bash
make migrate
```

---

### 5. `setup` — полная настройка проекта

```makefile
setup: install migrate fixtures users
	python manage.py collectstatic --noinput
	@echo "✅ Проект настроен!"
```

**Зависимости:** Сначала выполнятся `install`, `migrate`, `fixtures`, `users`.

**Порядок выполнения:**
1. `make install` → установка pip пакетов
2. `make migrate` → миграции БД
3. `make fixtures` → загрузка тестовых данных
4. `make users` → создание тестовых пользователей
5. `collectstatic` → сбор статики
6. Вывод сообщения об успехе

**Использование:**
```bash
make setup  # Одна команда вместо 5-6 отдельных!
```

---

### 6. `clean` — очистка временных файлов

```makefile
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
```

**Что делает:**
- Удаляет скомпилированные Python файлы (`*.pyc`, `*.pyo`)
- Удаляет кеш директории (`__pycache__`)
- Удаляет логи и кеш тестов

**Команды:**
- `find . -type d -name "__pycache__"` — найти все директории с именем `__pycache__`
- `-exec rm -rf {} +` — удалить найденные директории
- `find . -type f -name "*.pyc" -delete` — найти и удалить все `.pyc` файлы

---

### 7. Docker команды

```makefile
docker-build:
	docker-compose build

docker-up:
	docker-compose up -d
	docker-compose exec web python manage.py migrate
	docker-compose exec web python manage.py loaddata fixtures/initial_data.json
	docker-compose exec web python manage.py create_test_users

docker-down:
	docker-compose down
```

**`docker-build`** — собирает Docker образ из Dockerfile  
**`docker-up`** — запускает контейнеры и настраивает БД  
**`docker-down`** — останавливает и удаляет контейнеры

**Флаг `-d`** — запуск в фоновом режиме (detached mode)

---

## 🎓 Продвинутые концепции

### Переменные в Makefile

```makefile
# Определение переменных
PYTHON = python3
MANAGE = $(PYTHON) manage.py
PIP = pip3

# Использование переменных
install:
	$(PIP) install -r requirements.txt

migrate:
	$(MANAGE) makemigrations
	$(MANAGE) migrate
```

**Преимущество:** Легко изменить версию Python в одном месте.

---

### Условия в Makefile

```makefile
install:
ifeq ($(OS),Windows_NT)
	pip install -r requirements.txt
else
	pip3 install -r requirements.txt
endif
```

**Применение:** Разные команды для Windows и Linux/Mac.

---

### Автоматические переменные

```makefile
build: main.c utils.c
	gcc $^ -o $@
```

**`$^`** — все зависимости (main.c utils.c)  
**`$@`** — имя цели (build)  
**`$<`** — первая зависимость (main.c)

---

### Паттерны (pattern rules)

```makefile
# Компиляция всех .c файлов в .o
%.o: %.c
	gcc -c $< -o $@
```

**`%`** — подстановочный символ (wildcard).

---

## 🚀 Примеры использования в реальных проектах

### Django проект (расширенный)

```makefile
.PHONY: help install dev prod test coverage clean lint format

PYTHON := python3
MANAGE := $(PYTHON) manage.py
VENV := venv
BIN := $(VENV)/bin

help:
	@echo "Django Project Commands:"
	@echo "  make install    - Setup project"
	@echo "  make dev        - Run development server"
	@echo "  make prod       - Run production server"
	@echo "  make test       - Run tests"
	@echo "  make coverage   - Test coverage report"
	@echo "  make lint       - Check code quality"
	@echo "  make format     - Format code"

install:
	$(PYTHON) -m venv $(VENV)
	$(BIN)/pip install --upgrade pip
	$(BIN)/pip install -r requirements.txt
	$(BIN)/$(MANAGE) migrate
	@echo "✅ Project installed!"

dev:
	$(BIN)/$(MANAGE) runserver 0.0.0.0:8000

prod:
	gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4

test:
	$(BIN)/pytest -v

coverage:
	$(BIN)/pytest --cov=apps --cov-report=html
	@echo "Open htmlcov/index.html in browser"

lint:
	$(BIN)/flake8 apps/
	$(BIN)/pylint apps/

format:
	$(BIN)/black apps/
	$(BIN)/isort apps/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf htmlcov .coverage .pytest_cache
	@echo "✅ Cleaned!"

migrations:
	$(BIN)/$(MANAGE) makemigrations
	$(BIN)/$(MANAGE) migrate

superuser:
	$(BIN)/$(MANAGE) createsuperuser

shell:
	$(BIN)/$(MANAGE) shell_plus

db-reset:
	rm -f db.sqlite3
	$(BIN)/$(MANAGE) migrate
	$(BIN)/$(MANAGE) loaddata fixtures/*.json

backup:
	$(BIN)/$(MANAGE) dumpdata --indent=2 > backup_$(shell date +%Y%m%d_%H%M%S).json

deploy:
	git pull origin main
	$(BIN)/pip install -r requirements.txt
	$(BIN)/$(MANAGE) migrate
	$(BIN)/$(MANAGE) collectstatic --noinput
	sudo systemctl restart gunicorn
	@echo "✅ Deployed!"
```

---

### React проект

```makefile
.PHONY: install dev build test clean

install:
	npm install

dev:
	npm run dev

build:
	npm run build

test:
	npm test

lint:
	npm run lint

format:
	npm run format

clean:
	rm -rf node_modules dist build
```

---

### Python библиотека

```makefile
.PHONY: install test publish clean

install:
	pip install -e .
	pip install -r requirements-dev.txt

test:
	pytest tests/ -v

test-all:
	tox

coverage:
	pytest --cov=mylib --cov-report=html

lint:
	flake8 mylib/
	mypy mylib/

format:
	black mylib/ tests/
	isort mylib/ tests/

build:
	python -m build

publish: build
	twine upload dist/*

clean:
	rm -rf build dist *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} +
```

---

## 💡 Best Practices

### 1. Всегда добавляйте `help`

```makefile
help:
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  make %-15s %s\n", $$1, $$2}'

install: ## Install dependencies
	pip install -r requirements.txt

test: ## Run tests
	pytest
```

**Результат `make help`:**
```
Available commands:
  make install        Install dependencies
  make test           Run tests
```

---

### 2. Используйте переменные для гибкости

```makefile
ENV ?= development
PORT ?= 8000

run:
	DJANGO_ENV=$(ENV) python manage.py runserver $(PORT)
```

**Использование:**
```bash
make run                    # development:8000
make run ENV=production     # production:8000
make run PORT=9000          # development:9000
```

---

### 3. Безопасное удаление

```makefile
clean:
	@echo "⚠️  Deleting cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Done!"
```

**`2>/dev/null`** — скрывает ошибки  
**`|| true`** — продолжает выполнение даже при ошибках

---

### 4. Проверка зависимостей

```makefile
check-docker:
	@which docker > /dev/null || (echo "❌ Docker not installed" && exit 1)

docker-build: check-docker
	docker-compose build
```

---

## 🐛 Частые ошибки

### 1. ❌ Пробелы вместо TAB

```makefile
# НЕПРАВИЛЬНО (пробелы)
install:
    pip install -r requirements.txt

# ПРАВИЛЬНО (TAB)
install:
	pip install -r requirements.txt
```

**Ошибка:**
```
Makefile:2: *** missing separator. Stop.
```

---

### 2. ❌ Забыли `.PHONY`

```makefile
# Если есть файл test.py
test:
	pytest

# make test скажет: 'test' is up to date
```

**Решение:**
```makefile
.PHONY: test

test:
	pytest
```

---

### 3. ❌ Неправильные зависимости

```makefile
# Зациклится!
a: b
b: a
```

---

## 🔍 Полезные команды

### Показать все цели

```bash
make -qp | awk -F':' '/^[a-zA-Z0-9][^$#\/\t=]*:([^=]|$)/ {split($1,A,/ /);for(i in A)print A[i]}'
```

### Dry-run (не выполнять, только показать)

```bash
make -n install  # Покажет команды, но не выполнит
```

### Игнорировать ошибки

```bash
make -i test  # Продолжит даже если тесты упадут
```

### Параллельное выполнение

```bash
make -j4 test  # Запустит 4 задачи параллельно
```

---

## 📚 Дополнительные ресурсы

**Официальная документация:**
- https://www.gnu.org/software/make/manual/

**Туториалы:**
- https://makefiletutorial.com/
- https://opensource.com/article/18/8/what-how-makefile

**Cheat Sheet:**
- https://devhints.io/makefile

---

## 🎯 Практическое задание

Создайте Makefile для Django проекта с командами:

1. `make install` — установка зависимостей
2. `make dev` — запуск dev сервера
3. `make test` — запуск тестов с coverage
4. `make lint` — проверка кода (flake8)
5. `make format` — форматирование (black)
6. `make docker` — сборка и запуск в Docker
7. `make clean` — очистка кеша
8. `make help` — справка

**Бонус:** Добавьте автоматическую проверку виртуального окружения.

---

## ✅ Итоги

**Makefile** — это:
✅ Автоматизация рутины  
✅ Документация команд проекта  
✅ Стандартизация workflow  
✅ Экономия времени команды  
✅ Уменьшение ошибок  

**Для Django разработчика знание Makefile — это must-have навык уровня Middle.**

---
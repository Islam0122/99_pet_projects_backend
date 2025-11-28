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
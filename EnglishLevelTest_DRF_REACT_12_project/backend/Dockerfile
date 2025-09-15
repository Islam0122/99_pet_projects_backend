# Используем официальный Python
FROM python:3.13-slim

# Устанавливаем зависимости
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

# Копируем файлы проекта
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /code/

# Собираем статику
RUN python manage.py collectstatic --noinput --settings=config.settings.production

# Команда запуска Gunicorn
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]

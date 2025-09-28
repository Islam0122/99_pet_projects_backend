FROM python:3.13-slim

# Системные зависимости для WeasyPrint
RUN apt-get update && apt-get install -y \
    libcairo2 \
    libcairo2-dev \
    libpango-1.0-0 \
    libpango1.0-dev \
    libgdk-pixbuf-xlib-2.0-0 \
    libgdk-pixbuf-xlib-2.0-dev \
    libffi-dev \
    build-essential \
    shared-mime-info \
    fontconfig \
    python3-cffi \
    && rm -rf /var/lib/apt/lists/*

RUN pip install celery


WORKDIR /code

# Установка зависимостей Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование проекта
COPY . .

# Создание папок для медиа и логов
RUN mkdir -p /code/media /code/logs

# Команда запуска Django через Gunicorn
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "1"]

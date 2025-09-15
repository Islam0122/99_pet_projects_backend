FROM python:3.13-slim

# Устанавливаем системные библиотеки для WeasyPrint
RUN apt-get update && apt-get install -y \
    libcairo2 \
    libcairo2-dev \
    libpango-1.0-0 \
    libpango1.0-dev \
    libgdk-pixbuf2.0-0 \
    libgdk-pixbuf2.0-dev \
    libffi-dev \
    shared-mime-info \
    python3-cffi \
    build-essential \
    fontconfig \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

# Устанавливаем зависимости Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Создаём папки для медиа и логов
RUN mkdir -p /code/media /code/logs

# Запуск Django через Gunicorn
CMD ["gunicorn", "config.]()

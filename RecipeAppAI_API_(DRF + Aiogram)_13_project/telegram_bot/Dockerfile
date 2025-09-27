# Используем Python 3.11 slim
FROM python:3.11-slim

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Экспорт переменных окружения (пример)
ENV PYTHONUNBUFFERED=1
ENV ENV=production

# Команда запуска (можно потом переопределять в docker-compose)
CMD ["python", "main.py"]

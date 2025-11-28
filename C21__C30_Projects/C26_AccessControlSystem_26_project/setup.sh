#!/bin/bash

echo "🚀 Настройка проекта Access Control System..."

if [ ! -d "venv" ]; then
    echo "📦 Создание виртуального окружения..."
    python3 -m venv venv
fi

echo "🔌 Активация виртуального окружения..."
source venv/bin/activate

echo "📥 Установка зависимостей..."
pip install --upgrade pip
pip install -r requirements.txt

if [ ! -f ".env" ]; then
    echo "📝 Создание .env файла..."
    cp .env.example .env
    echo "⚠️  ВАЖНО: Отредактируйте .env файл с вашими настройками!"
fi

mkdir -p fixtures

echo "🗄️  Выполнение миграций..."
python manage.py makemigrations
python manage.py migrate


echo "📊 Загрузка тестовых данных..."
python manage.py loaddata fixtures/initial_data.json

echo "👥 Создание тестовых пользователей..."
python manage.py create_test_users

echo "🎨 Сбор статических файлов..."
python manage.py collectstatic --noinput

echo ""
echo "✅ Проект успешно настроен!"
echo ""
echo "📋 Тестовые пользователи:"
echo "   1. admin@example.com / admin123 (Администратор)"
echo "   2. manager@example.com / manager123 (Менеджер)"
echo "   3. user@example.com / user123 (Пользователь)"
echo "   4. guest@example.com / guest123 (Гость)"
echo ""
echo "🌐 Для запуска сервера выполните:"
echo "   python manage.py runserver"
echo ""
echo "📚 API документация будет доступна по адресу:"
echo "   http://localhost:8000/api/swagger/"
echo ""
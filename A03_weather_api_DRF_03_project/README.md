# Weather API (Django REST Framework)

API погоды, которое извлекает и возвращает данные о погоде через сторонний API Visual Crossing с кэшированием через Redis.

## Возможности
- Получение текущей погоды по названию города.
- Кэширование данных в Redis (по умолчанию 12 часов) для ускорения повторных запросов.
- Проверка и обработка ошибок стороннего API.
- Возвращает температуру, влажность, скорость ветра и описание условий.

## Технологии
- Python 3.13
- Django 5 + Django REST Framework
- Redis
- Requests
- Docker (опционально)

## Установка и запуск
1. Клонируйте репозиторий:
```bash
git clone https://github.com/Islam0122/weather_api_DRF_03_project.git
cd weather_api_DRF_03_project
````

2. Установите зависимости:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Настройте `.env` файл:

```
ALLOWED_HOSTS=
CORS_ALLOWED_ORIGINS=
DEBUG=
DJANGO_ENV=
EMAIL_BACKEND=
EMAIL_HOST=
EMAIL_HOST_PASSWORD=
EMAIL_HOST_USER=
EMAIL_PORT=
EMAIL_USE_TLS=
SECRET_KEY=
WEATHER_API_URL=https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline
WEATHER_API_KEY=YOUR_VISUAL_CROSSING_KEY
REDIS_URL=redis://127.0.0.1:6379/1
```

4. Запустите Redis локально или через Docker:

```bash
docker run -d -p 6379:6379 redis
```

5. Запустите сервер Django:

```bash
python manage.py runserver
```

## Примеры запросов

### Получить погоду по городу

**GET** `/api/weather/?city=Bishkek`

**Пример ответа:**

```json
{
  "city": "Bishkek",
  "temperature": 25.3,
  "humidity": 60,
  "windspeed": 10,
  "conditions": "Sunny",
  "source": "api"
}
```

**Пример кэша (при повторном запросе):**

```json
{
  "city": "Bishkek",
  "temperature": 25.3,
  "humidity": 60,
  "windspeed": 10,
  "conditions": "Sunny",
  "source": "cache"
}
```

## Тестирование

* Запуск тестов Django:

```bash
python manage.py test
```

* Тесты проверяют:

  * Статус ответа
  * Наличие всех полей
  * Типы данных и диапазоны
  * Источник данных (API или кэш)
  * Производительность при кэшировании

## Примечания

* Убедитесь, что Redis запущен, чтобы ускорить ответы API.
* API может возвращать ошибки при недоступности внешнего сервиса Visual Crossing.
* Для продвинутого уровня можно реализовать Rate Limiting (ограничение количества запросов).


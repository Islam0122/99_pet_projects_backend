import os
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.core.cache import cache

WEATHER_API_URL = os.getenv("WEATHER_API_URL")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
CACHE_TIMEOUT = 12 * 60 * 60  # 12 часов

@api_view(['GET'])
def weather_view(request):
    city = request.GET.get("city")
    if not city:
        return Response({"error": "City parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        cached_data = cache.get(city.lower())
    except Exception:
        cached_data = None

    if cached_data:
        cached_data["source"] = "cache"
        return Response(cached_data, status=status.HTTP_200_OK)

    url = f"{WEATHER_API_URL}/{city}?unitGroup=metric&key={WEATHER_API_KEY}&contentType=json"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            return Response({"error": "Weather API error"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        data = response.json()
        current = data.get("currentConditions")
        if not current:
            return Response({"error": "No current weather data"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        temperature = float(current.get("temp", 0))
        humidity = float(current.get("humidity", 0))
        humidity = max(0, min(humidity, 100))
        windspeed = float(current.get("windspeed", 0))
        conditions = current.get("conditions", "")

        weather_data = {
            "city": city,
            "temperature": temperature,
            "conditions": conditions,
            "humidity": humidity,
            "windspeed": windspeed,
            "source": "api"
        }

        try:
            cache.set(city.lower(), weather_data, timeout=CACHE_TIMEOUT)
        except Exception:
            pass

        return Response(weather_data, status=status.HTTP_200_OK)

    except requests.exceptions.RequestException:
        return Response({"error": "Unable to fetch weather data"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

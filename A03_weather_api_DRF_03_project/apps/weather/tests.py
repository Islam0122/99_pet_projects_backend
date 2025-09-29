from django.test import TestCase
from rest_framework.test import APIClient
from django.core.cache import cache
import time

class WeatherAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        cache.clear()

    def test_weather_cities(self):
        cities = ["Bishkek", "London", "New York"]
        for city in cities:
            with self.subTest(city=city):
                # Первый запрос – API
                start = time.time()
                response = self.client.get(f"/api/weather/?city={city}")
                duration = time.time() - start

                self.assertEqual(response.status_code, 200)
                data = response.json()

                for field in ["city", "temperature", "humidity", "windspeed", "conditions", "source"]:
                    self.assertIn(field, data)

                self.assertIsInstance(data["temperature"], (int, float))
                self.assertIsInstance(data["humidity"], (int, float))
                self.assertIsInstance(data["windspeed"], (int, float))
                self.assertIsInstance(data["conditions"], str)
                self.assertTrue(-100 <= data["temperature"] <= 100)
                self.assertTrue(0 <= data["humidity"] <= 100)

                self.assertIn(data["source"], ["api", "cache"])

                print(f"{city} response time: {duration*1000:.0f}ms")

                response_cache = self.client.get(f"/api/weather/?city={city}")
                data_cache = response_cache.json()
                self.assertEqual(data_cache["source"], "cache")

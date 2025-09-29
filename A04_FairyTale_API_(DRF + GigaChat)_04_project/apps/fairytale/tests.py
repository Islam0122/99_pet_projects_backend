from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.fairytale.models import FairyTale


class FairyTaleAPITestCase(APITestCase):
    def setUp(self):
        # Создаем одну сказку вручную
        self.fairytale = FairyTale.objects.create(
            title="Тестовая сказка",
            story="Жил-был тестовый герой..."
        )
        self.url = reverse("fairytales")

    def test_get_fairytales_list(self):
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if "results" in response.data:
            results = response.data["results"]
        else:
            results = response.data

        self.assertIsInstance(results, list)
        self.assertGreaterEqual(len(results), 1)
        self.assertIn("title", results[0])
        self.assertIn("story", results[0])

    def test_create_fairytale(self):
        payload = {
            "title": "islam",
            "characters": ["islam dev"],
            "style": "сказочный",
            "length": "medium"
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(FairyTale.objects.filter(title="islam").exists())
        self.assertIn("story", response.data)
        self.assertEqual(response.data["title"], "islam")

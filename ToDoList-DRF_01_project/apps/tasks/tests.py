import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from apps.tasks.models import Task

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def sample_task():
    return Task.objects.create(title="Test Task", description="Just a test")

@pytest.mark.django_db
def test_create_task(api_client):
    url = reverse("task-list")
    data = {"title": "New Task", "description": "Description"}
    response = api_client.post(url, data, format="json")
    assert response.status_code == 201
    assert response.data["title"] == "New Task"

@pytest.mark.django_db
def test_get_task(api_client, sample_task):
    url = reverse("task-detail", args=[sample_task.id])
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["title"] == sample_task.title

@pytest.mark.django_db
def test_get_tasks_list(api_client, sample_task):
    url = reverse("task-list")
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) > 0

@pytest.mark.django_db
def test_update_task(api_client, sample_task):
    url = reverse("task-detail", args=[sample_task.id])
    data = {"status": "completed"}
    response = api_client.patch(url, data, format="json")
    assert response.status_code == 200
    assert response.data["status"] == "completed"

@pytest.mark.django_db
def test_delete_task(api_client, sample_task):
    url = reverse("task-detail", args=[sample_task.id])
    response = api_client.delete(url)
    assert response.status_code == 204
    assert not Task.objects.filter(id=sample_task.id).exists()

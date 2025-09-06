from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from apps.user.models import User
from apps.contactbook.models import ContactBook

class ContactBookAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="islam",
            email="islam@example.com",
            password="strongpassword123"
        )
        self.client.login(email="islam@example.com", password="strongpassword123")
        self.contact_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "phone": "+1234567890",
            "address": "Some Street 123",
            "tags": "friend,work"
        }
        self.url = reverse('contacts-list')  # /contacts/

    def test_create_contact(self):
        response = self.client.post(self.url, self.contact_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContactBook.objects.count(), 1)
        self.assertEqual(ContactBook.objects.get().first_name, "John")

    def test_list_contacts(self):
        ContactBook.objects.create(owner=self.user, **self.contact_data)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_contact(self):
        contact = ContactBook.objects.create(owner=self.user, **self.contact_data)
        url = reverse('contacts-detail', args=[contact.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], "John")

    def test_update_contact(self):
        contact = ContactBook.objects.create(owner=self.user, **self.contact_data)
        url = reverse('contacts-detail', args=[contact.id])
        response = self.client.patch(url, {"first_name": "Jane"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        contact.refresh_from_db()
        self.assertEqual(contact.first_name, "Jane")

    def test_delete_contact(self):
        contact = ContactBook.objects.create(owner=self.user, **self.contact_data)
        url = reverse('contacts-detail', args=[contact.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ContactBook.objects.count(), 0)

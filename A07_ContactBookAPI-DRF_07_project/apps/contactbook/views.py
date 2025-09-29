from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import ContactBook
from .serializers import ContactBookSerializer


class ContactBookViewSet(viewsets.ModelViewSet):
    serializer_class = ContactBookSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['tags']
    search_fields = ['first_name', 'last_name', 'email', 'phone']

    def get_queryset(self):
        # Показываем только контакты текущего пользователя
        return ContactBook.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Привязываем контакт к текущему пользователю
        serializer.save(owner=self.request.user)


from rest_framework import viewsets, permissions
from .models import ContactBook
from .serializers import ContactBookSerializer

class ContactBookViewSet(viewsets.ModelViewSet):
    serializer_class = ContactBookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ContactBook.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

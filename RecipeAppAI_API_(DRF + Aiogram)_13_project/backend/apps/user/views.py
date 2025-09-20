from rest_framework import viewsets
from .models import TgUser
from .serializers import TgUserSerializer

class TgUserViewSet(viewsets.ModelViewSet):
    queryset = TgUser.objects.all()
    serializer_class = TgUserSerializer

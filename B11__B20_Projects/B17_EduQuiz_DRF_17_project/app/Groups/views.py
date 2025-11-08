from rest_framework import viewsets
from rest_framework import permissions
from .models import Student, Group
from .serializers import StudentSerializer, GroupSerializer

class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Разрешает просмотр всем, но изменять данные могут только авторизованные пользователи.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True
        return request.user and request.user.is_authenticated

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]



class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]



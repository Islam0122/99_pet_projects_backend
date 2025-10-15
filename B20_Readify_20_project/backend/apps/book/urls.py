from django.urls import path
from .views import LibRuBookView

urlpatterns = [
    path("books/", LibRuBookView.as_view(), name="books"),
]

from django.urls import path
from .views import QueryBookView

urlpatterns = [
    path('query/', QueryBookView.as_view(), name='query-book'),
]

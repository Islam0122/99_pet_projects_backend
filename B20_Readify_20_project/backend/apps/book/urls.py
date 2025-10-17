from django.urls import path
from .views import BookListAPIView, ChapterDetailAPIView, LoadBookAPIView

urlpatterns = [
    path('books/', BookListAPIView.as_view(), name="books-list"),
    path('books/<int:book_id>/chapters/<int:chapter_number>/', ChapterDetailAPIView.as_view(), name="chapter-detail"),
    path('books/load/', LoadBookAPIView.as_view(), name="load-book"),
]

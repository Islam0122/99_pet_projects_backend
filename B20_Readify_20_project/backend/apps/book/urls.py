from django.urls import path,include
from .views import BookListAPIView, ChapterDetailAPIView, LoadBookAPIView, UserBookViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"user-books", UserBookViewSet, basename="user-books")


urlpatterns = [
    path('books/', BookListAPIView.as_view(), name="books-list"),
    path('books/<int:book_id>/chapters/<int:chapter_number>/', ChapterDetailAPIView.as_view(), name="chapter-detail"),
    path('books/load/', LoadBookAPIView.as_view(), name="load-book"),
    path('', include(router.urls)),
    ]

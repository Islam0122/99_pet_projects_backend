from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'chapters', ChapterViewSet, basename='chapter')
router.register(r'user-books', UserBookViewSet, basename='userbook')

urlpatterns = [
    path('', include(router.urls)),
    path('books-list/', BookListAPIView.as_view(), name='books-list'),
    path('books/<int:book_id>/chapters/<int:chapter_number>/', ChapterDetailAPIView.as_view(), name='chapter-detail'),
    path('load-book/', LoadBookAPIView.as_view(), name='load-book'),

    path('books/<int:pk>/chapters/', BookViewSet.as_view({'get': 'chapters'}), name='book-chapters'),
    path('books/<int:pk>/chapter/<int:chapter_number>/', BookViewSet.as_view({'get': 'chapter'}), name='book-chapter'),
]
from django.urls import path
from .views import (
    VideoListView, VideoDetailView,
    VideoCategoryListView, VideoCategoryDetailView
)

urlpatterns = [
    path('videos/', VideoListView.as_view(), name='video-list'),
    path('videos/<int:pk>/', VideoDetailView.as_view(), name='video-detail'),
    path('videos_categories/', VideoCategoryListView.as_view(), name='category-list'),
    path('videos_categories/<int:pk>/', VideoCategoryDetailView.as_view(), name='category-detail'),
]

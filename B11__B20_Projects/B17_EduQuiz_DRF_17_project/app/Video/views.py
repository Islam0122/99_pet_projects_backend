from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Video, VideoCategory
from .serializers import VideoSerializer, VideoCategorySerializer

class VideoListView(APIView):
    def get(self, request):
        category_title = request.query_params.get('category')
        videos = Video.objects.filter(is_active=True)
        if category_title:
            videos = videos.filter(video_category__title__icontains=category_title)

        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VideoDetailView(APIView):
    def get(self, request, pk):
        try:
            video = Video.objects.get(pk=pk, is_active=True)
        except Video.DoesNotExist:
            return Response({"detail": "Видео не найдено."}, status=status.HTTP_404_NOT_FOUND)

        serializer = VideoSerializer(video)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VideoCategoryListView(APIView):
    def get(self, request):
        categories = VideoCategory.objects.all()
        serializer = VideoCategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VideoCategoryDetailView(APIView):
    def get(self, request, pk):
        try:
            category = VideoCategory.objects.get(pk=pk)
        except VideoCategory.DoesNotExist:
            return Response({"detail": "Категория не найдена."}, status=status.HTTP_404_NOT_FOUND)

        serializer = VideoCategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

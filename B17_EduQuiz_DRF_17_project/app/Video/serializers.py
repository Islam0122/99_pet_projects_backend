from rest_framework import serializers
from .models import Video, VideoCategory

class VideoCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoCategory
        fields = '__all__'

class VideoSerializer(serializers.ModelSerializer):
    video_category = serializers.PrimaryKeyRelatedField(
        queryset=VideoCategory.objects.all(),
        write_only=True  # При создании/обновлении ожидается ID категории
    )
    video_category_info = VideoCategorySerializer(
        source='video_category', read_only=True  # При получении данных возвращает объект
    )

    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'video_category', 'video_category_info', 'video_url', 'created_at', 'is_active']
        read_only_fields = ['created_at']

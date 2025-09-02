from rest_framework import serializers
from .models import Post, Category, Tag

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title", "slug"]

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "title", "slug"]

class PostSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        write_only=True,
        source="category"
    )
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        write_only=True,
        source="tags"
    )

    class Meta:
        model = Post
        fields = [
            "id", "title", "content", "category", "category_id",
            "tags", "tag_ids", "slug", "created_at", "updated_at"
        ]
        read_only_fields = ["id", "slug", "created_at", "updated_at"]

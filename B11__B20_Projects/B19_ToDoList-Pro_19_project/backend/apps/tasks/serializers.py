from rest_framework import serializers
from .models import Task, Category
from ..accounts.serializers import TGUserSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "created_at"]
        read_only_fields = ["created_at"]


class TaskSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True,
        write_only=True,
        source="categories",
        required=False,
        help_text="Выберите категории для задачи"
    )
    created_at = serializers.SerializerMethodField()
    due_date_formatted = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "owner",
            "categories",
            "category_ids",
            "created_at",
            "due_date",
            "due_date_formatted",
            "done"
        ]
        read_only_fields = [ "id","created_at"]


    def get_created_at(self, obj):
        return obj.created_at.strftime("%d.%m.%Y %H:%M")

    def get_due_date_formatted(self, obj):
        if obj.due_date:
            return obj.due_date.strftime("%d.%m.%Y %H:%M")
        return None


from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "title")


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    sales = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id",
            "identification_number",
            "title",
            "description",
            "category",
            "price",
            "sale_price",
            "image",
            "is_archived",
            "created_at",
            "updated_at",
            "sales",
        )
        read_only_fields = ("created_at", "updated_at")

    def get_sales(self, obj):
        if obj.price and obj.sale_price:
            discount_percent = ((obj.price - obj.sale_price) / obj.price) * 100
            return round(discount_percent, 2)  # например 15.0
        return 0


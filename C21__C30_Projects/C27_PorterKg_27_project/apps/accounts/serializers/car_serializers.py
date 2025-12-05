from rest_framework import serializers
from ..models import Car, CarImage
from datetime import datetime


class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = [
            'id',
            'image',
            'is_primary',
            'order',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def validate_image(self, value):
        """Валидация размера изображения"""
        if value.size > 5 * 1024 * 1024:  # 5MB
            raise serializers.ValidationError(
                "Размер изображения не должен превышать 5MB"
            )
        return value


class CarSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(
        read_only=True
    )
    primary_image = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = [
            'id',
            'marka',
            'model',
            'full_name',
            'color',
            'year',
            'number_plate',
            'fuel_type',
            'max_passengers',
            'is_active',
            'primary_image',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def get_primary_image(self, obj):
        primary = obj.images.filter(is_primary=True).first()
        if primary:
            return CarImageSerializer(primary).data
        return None

    def validate_year(self, value):
        current_year = datetime.now().year
        if value < 1900:
            raise serializers.ValidationError(
                "Год выпуска не может быть меньше 1900"
            )
        if value > current_year + 1:
            raise serializers.ValidationError(
                f"Год выпуска не может быть больше {current_year + 1}"
            )
        return value

    def validate_number_plate(self, value):
        value = value.upper().strip()
        if not value:
            raise serializers.ValidationError(
                "Номерной знак не может быть пустым"
            )
        return value


class CarDetailSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(
        read_only=True
    )
    images = CarImageSerializer(many=True, read_only=True)
    has_images = serializers.BooleanField(
        read_only=True
    )

    class Meta:
        model = Car
        fields = [
            'id',
            'marka',
            'model',
            'full_name',
            'color',
            'year',
            'number_plate',
            'vin_code',
            'fuel_type',
            'max_passengers',
            'description',
            'is_active',
            'images',
            'has_images',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id',
            'images',
            'has_images',
            'created_at',
            'updated_at'
        ]


class CarCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = [
            'marka',
            'model',
            'color',
            'year',
            'number_plate',
            'vin_code',
            'fuel_type',
            'max_passengers',
            'description',
        ]

    def validate_vin_code(self, value):
        if value:
            value = value.upper().strip()
            if len(value) not in [0, 17]:
                raise serializers.ValidationError(
                    "VIN-код должен состоять из 17 символов"
                )
        return value


class CarImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True)
    is_primary = serializers.BooleanField(default=False)
    order = serializers.IntegerField(default=0)

    def validate_image(self, value):
        if value.size > 5 * 1024 * 1024:  # 5MB
            raise serializers.ValidationError(
                "Размер изображения не должен превышать 5MB"
            )

        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
        if value.content_type not in allowed_types:
            raise serializers.ValidationError(
                "Поддерживаются только форматы: JPEG, PNG, WebP"
            )

        return value

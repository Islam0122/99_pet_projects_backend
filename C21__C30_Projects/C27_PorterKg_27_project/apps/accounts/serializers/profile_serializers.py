from rest_framework import serializers
from ..models import GuestProfile, DriverProfile
from .user_serializers import UserSerializer, UserMinimalSerializer
from .car_serializers import CarDetailSerializer


class GuestProfileSerializer(serializers.ModelSerializer):
    user = UserMinimalSerializer(read_only=True)

    class Meta:
        model = GuestProfile
        fields = [
            'id',
            'user',
            'avatar',
            'bio',
            'phone_number',
            'birth_date',
            'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']

    def validate_phone_number(self, value):
        if value and not value.startswith('+'):
            raise serializers.ValidationError(
                "Номер телефона должен начинаться с '+'"
            )
        return value


class GuestProfileDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    has_complete_profile = serializers.BooleanField(
        read_only=True
    )

    class Meta:
        model = GuestProfile
        fields = [
            'id',
            'user',
            'avatar',
            'bio',
            'phone_number',
            'birth_date',
            'has_complete_profile',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id',
            'user',
            'has_complete_profile',
            'created_at',
            'updated_at'
        ]


class DriverProfileSerializer(serializers.ModelSerializer):
    user = UserMinimalSerializer(read_only=True)

    class Meta:
        model = DriverProfile
        fields = [
            'id',
            'user',
            'phone_number',
            'bio',
            'rating',
            'total_trips',
            'experience_years',
            'verified_driver',
            'driver_license_number',
            'driver_license_category',
            'created_at'
        ]
        read_only_fields = [
            'id',
            'user',
            'rating',
            'total_trips',
            'verified_driver',
            'created_at'
        ]

    def validate_phone_number(self, value):
        if value and not value.startswith('+'):
            raise serializers.ValidationError(
                "Номер телефона должен начинаться с '+'"
            )
        return value

    def validate_experience_years(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Стаж вождения не может быть отрицательным"
            )
        if value > 100:
            raise serializers.ValidationError(
                "Стаж вождения не может превышать 100 лет"
            )
        return value


class DriverProfileDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    car = CarDetailSerializer(read_only=True)
    has_complete_profile = serializers.BooleanField(
        read_only=True
    )

    class Meta:
        model = DriverProfile
        fields = [
            'id',
            'user',
            'phone_number',
            'bio',
            'rating',
            'total_trips',
            'experience_years',
            'verified_driver',
            'driver_license_number',
            'driver_license_category',
            'driver_license_expiry',
            'car',
            'has_complete_profile',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id',
            'user',
            'rating',
            'total_trips',
            'verified_driver',
            'car',
            'has_complete_profile',
            'created_at',
            'updated_at'
        ]


class DriverPublicSerializer(serializers.ModelSerializer):
    user = UserMinimalSerializer(read_only=True)
    car = CarDetailSerializer(read_only=True)

    class Meta:
        model = DriverProfile
        fields = [
            'id',
            'user',
            'bio',
            'rating',
            'total_trips',
            'experience_years',
            'verified_driver',
            'car'
        ]
        read_only_fields = fields
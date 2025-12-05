from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(
        read_only=True
    )

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'role',
            'is_verified',
            'auth_type',
            'created_at'
        ]
        read_only_fields = [
            'id',
            'email',
            'role',
            'auth_type',
            'created_at'
        ]


class UserDetailSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(
        read_only=True
    )
    is_driver = serializers.BooleanField(
        read_only=True
    )
    is_guest = serializers.BooleanField(
        read_only=True
    )

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'role',
            'is_verified',
            'auth_type',
            'is_active',
            'is_driver',
            'is_guest',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id',
            'email',
            'role',
            'auth_type',
            'is_verified',
            'is_active',
            'created_at',
            'updated_at'
        ]

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance


class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
        ]
        read_only_fields = fields
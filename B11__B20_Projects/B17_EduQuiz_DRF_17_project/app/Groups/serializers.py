from rest_framework import serializers
from .models import Student, Group

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'full_name', 'is_active', 'group', 'created_at', 'updated_at', 'created_by', 'updated_user')
        read_only_fields = ('created_at', 'updated_at', 'created_by', 'updated_user')

    def create(self, validated_data):
        user = self.context['request'].user  # Получаем текущего пользователя из контекста
        student = Student.objects.create(created_by=user, updated_user=user, **validated_data)
        return student

    def update(self, instance, validated_data):
        user = self.context['request'].user  # Получаем текущего пользователя из контекста
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.updated_user = user  # Обновляем поле updated_user
        instance.save()
        return instance

class StudentInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'full_name', 'group', 'is_active', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

class GroupSerializer(serializers.ModelSerializer):
    students = StudentInlineSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ('id', 'name', 'created_at', 'updated_at', 'created_by', 'updated_user', 'students')
        read_only_fields = ('created_at', 'updated_at', 'created_by', 'updated_user')

    def create(self, validated_data):
        user = self.context['request'].user  # Получаем текущего пользователя из контекста
        group = Group.objects.create(created_by=user, updated_user=user, **validated_data)
        return group

    def update(self, instance, validated_data):
        user = self.context['request'].user  # Получаем текущего пользователя из контекста
        instance.name = validated_data.get('name', instance.name)
        instance.updated_user = user  # Обновляем поле updated_user
        instance.save()
        return instance

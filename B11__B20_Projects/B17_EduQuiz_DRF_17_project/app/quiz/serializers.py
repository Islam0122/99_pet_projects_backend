from rest_framework import serializers
from .models import Topic, Question


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "text", "image", "option_a", "option_b", "option_c", "option_d", "correct_answer", "topic"]

    def create(self, validated_data):
        user = self.context['request'].user  # Получаем текущего пользователя из контекста
        question = Question.objects.create(
            created_by=user, updated_user=user, **validated_data
        )
        return question

    def update(self, instance, validated_data):
        user = self.context['request'].user

        instance.text = validated_data.get('text', instance.text)
        instance.option_a = validated_data.get('option_a', instance.option_a)
        instance.option_b = validated_data.get('option_b', instance.option_b)
        instance.option_c = validated_data.get('option_c', instance.option_c)
        instance.option_d = validated_data.get('option_d', instance.option_d)
        instance.correct_answer = validated_data.get('correct_answer', instance.correct_answer)
        instance.topic = validated_data.get('topic', instance.topic)  # Обновление topic
        instance.image = validated_data.get('image', instance.image)  # Обновление изображения
        instance.updated_user = user
        instance.save()
        return instance




class TopicSerializer(serializers.ModelSerializer):
    difficulty_label = serializers.CharField(source="get_difficulty_display", read_only=True)
    questions_count = serializers.IntegerField(source="questions.count", read_only=True)
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Topic
        fields = ["id", "name", "description", "difficulty", "difficulty_label", "questions_count", "questions"]

    def create(self, validated_data):
        user = self.context['request'].user  # Получаем текущего пользователя из контекста
        topic = Topic.objects.create(created_by=user, updated_user=user, **validated_data)
        return topic

    def update(self, instance, validated_data):
        user = self.context['request'].user  # Получаем текущего пользователя из контекста
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.difficulty = validated_data.get('difficulty', instance.difficulty)
        instance.updated_user = user  # Обновляем поле updated_user
        instance.save()
        return instance


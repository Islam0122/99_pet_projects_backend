from django.core.cache import cache
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import UserRecipe
from .serializers import UserRecipeSerializer
from .gigachat_utils import sent_prompt_and_get_response


class UserRecipeViewSet(viewsets.ModelViewSet):
    queryset = UserRecipe.objects.all()
    serializer_class = UserRecipeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_text = serializer.validated_data.get("user_text")

        # Проверяем, есть ли готовый рецепт в кэше
        cache_key = f"user_recipe:{user_text}"
        ai_result = cache.get(cache_key)

        if not ai_result:
            prompt = f"""
            Ты — IslamDev AI, шеф-повар и контент-райтер. Отвечай на русском языке.
            У пользователя есть только эти ингредиенты: {user_text}.
            Составь подробный, красивый рецепт в формате Markdown:

            - Название блюда
            - Краткое описание (1-2 предложения)
            - Список ингредиентов с количествами
            - Пошаговая инструкция (каждый шаг отдельной строкой)
            - Общее время приготовления (prep + cook) и количество порций (2 по умолчанию)
            - Советы по сервировке и возможные заменители для аллергенов

            Используй метрические единицы (граммы, миллилитры), красиво оформляй заголовки, списки и шаги.
            Сделай текст максимально приятным для чтения пользователем.
            """

            ai_result = sent_prompt_and_get_response(prompt)

            cache.set(cache_key, ai_result, timeout=3600)

        # Создаём объект в БД
        user_recipe = UserRecipe.objects.create(
            user=serializer.validated_data["user"],
            category=serializer.validated_data.get("category"),
            user_text=user_text,
            ai_result=ai_result,
        )

        output_serializer = self.get_serializer(user_recipe)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

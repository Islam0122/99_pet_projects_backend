from django.core.cache import cache
from rest_framework import generics, status
from rest_framework.response import Response

from .models import FairyTale
from .serializers import FairyTaleSerializer, FairyTaleRequestSerializer
from .gigachat_utils import sent_prompt_and_get_response


class FairyTaleListCreateView(generics.ListCreateAPIView):
    queryset = FairyTale.objects.all()
    serializer_class = FairyTaleSerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
            return FairyTaleRequestSerializer
        return FairyTaleSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        cache_key = f"fairytale:{data['title']}:{data['style']}:{'-'.join(data['characters'])}:{data['length']}"

        cached_story = cache.get(cache_key)
        if cached_story:
            fairytale = FairyTale.objects.create(title=data["title"], story=cached_story)
            return Response(FairyTaleSerializer(fairytale).data, status=status.HTTP_201_CREATED)

        prompt = (
            f"Придумай сказку с заголовком '{data['title']}'. "
            f"Персонажи: {', '.join(data['characters'])}. "
            f"Стиль: {data['style']}. "
            f"Длина: {data['length']}."
        )

        # Запрашиваем у GigaChat
        story = sent_prompt_and_get_response(prompt)
        if story.startswith("Ошибка") or story.startswith("Не удалось"):
            return Response({"error": story}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Сохраняем в БД
        fairytale = FairyTale.objects.create(title=data["title"], story=story)

        # Кэшируем на 1 час
        cache.set(cache_key, story, timeout=3600)

        return Response(FairyTaleSerializer(fairytale).data, status=status.HTTP_201_CREATED)

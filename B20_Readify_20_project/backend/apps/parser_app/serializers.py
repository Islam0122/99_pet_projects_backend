from rest_framework import serializers

class ChunkSerializer(serializers.Serializer):
    idx = serializers.IntegerField()
    text = serializers.CharField()
    start = serializers.IntegerField()
    end = serializers.IntegerField()

class MetadataSerializer(serializers.Serializer):
    title = serializers.CharField(required=False, allow_null=True)
    author = serializers.CharField(required=False, allow_null=True)
    language = serializers.CharField(required=False, allow_null=True)

class ParseResultSerializer(serializers.Serializer):
    id = serializers.CharField()
    metadata = MetadataSerializer(required=False)
    full_text_length = serializers.IntegerField()
    chunks = ChunkSerializer(many=True)

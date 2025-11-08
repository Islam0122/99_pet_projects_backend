from rest_framework import serializers
from .models import ContactBook

class ContactBookSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ContactBook
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


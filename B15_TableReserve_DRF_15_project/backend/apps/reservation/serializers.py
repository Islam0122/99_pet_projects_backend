from rest_framework import serializers
from .models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_fields = ('user', 'status', 'created_at', 'updated_at')

    def validate(self, attrs):
        table = attrs['table']
        date = attrs['date']
        start = attrs['start_time']
        end = attrs['end_time']

        if Reservation.objects.filter(
                table=table,
                date=date,
                status__in=['pending', 'confirmed'],
                start_time__lt=end,
                end_time__gt=start
        ).exists():
            raise serializers.ValidationError("Этот столик уже занят в указанное время.")
        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['status'] = 'pending'
        return super().create(validated_data)

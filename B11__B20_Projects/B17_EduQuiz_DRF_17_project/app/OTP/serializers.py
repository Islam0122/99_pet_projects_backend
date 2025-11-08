from rest_framework import serializers
from .models import OTP

class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ['email', 'code']

    def validate_code(self, value):
        email = self.initial_data.get('email')
        otp = OTP.objects.filter(email=email, code=value).first()
        if not otp:
            raise serializers.ValidationError("Неверный OTP код или email.")
        return value
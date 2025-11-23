from datetime import timedelta
import random
from django.conf import settings
from django.utils import timezone
from rest_framework import serializers
from .models import UserModel, UserProfile
from .utils import send_otp


### 📌 **1. Сериализатор регистрации пользователя**
class UserRegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(
        write_only=True,
        min_length=settings.MIN_PASSWORD_LENGTH,
        required=False,
        error_messages={
            "min_length": f"Пароль должен содержать минимум {settings.MIN_PASSWORD_LENGTH} символов"
        },
    )
    password2 = serializers.CharField(
        write_only=True,
        min_length=settings.MIN_PASSWORD_LENGTH,
        required=False,
        error_messages={
            "min_length": f"Пароль должен содержать минимум {settings.MIN_PASSWORD_LENGTH} символов"
        },
    )

    class Meta:
        model = UserModel
        fields = (
            "id",
            "phone_number",
            "email",
            "otp",
            "password1",
            "password2",
        )
        read_only_fields = ("id",)

    def validate(self, data):
        # Убираем проверку на совпадение паролей, если они не обязательны
        if data.get("password1") and data.get("password2"):
            if data["password1"] != data["password2"]:
                raise serializers.ValidationError("Пароли не совпадают.")
        return data


    def create(self, validated_data):
        otp = random.randint(1000, 9999)
        otp_expiry = timezone.now() + timedelta(minutes=10)  # Время действия OTP

        # Создание пользователя с номером телефона, email и OTP
        user = UserModel.objects.create(
            phone_number=validated_data["phone_number"],
            email=validated_data.get("email"),
            otp=otp,
            otp_expiry=otp_expiry,
            max_otp_try=settings.MAX_OTP_TRY
        )

        # Если пароль передан, устанавливаем его
        if validated_data.get("password1"):
            user.set_password(validated_data["password1"])

        user.save()

        # Отправка OTP по SMS
        send_otp(validated_data["phone_number"], otp)
        return user


### 📌 **2. Сериализатор для подтверждения OTP-кода**
class OTPVerificationSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        max_length=15,
        required=True,
        error_messages={"required": "Введите номер телефона."}
    )
    otp = serializers.CharField(
        max_length=6,
        required=True,
        error_messages={"required": "Введите OTP-код из SMS."}
    )

    def validate(self, data):
        phone_number = data.get("phone_number")
        otp = data.get("otp")

        try:
            user = UserModel.objects.get(phone_number=phone_number)
        except UserModel.DoesNotExist:
            raise serializers.ValidationError("Пользователь с таким номером не найден.")

        # Проверка на количество попыток
        if int(user.max_otp_try) <= 0:
            # Проверка на время, когда был заблокирован пользователь (otp_max_out)
            if user.otp_max_out and timezone.now() < user.otp_max_out:
                raise serializers.ValidationError("Превышено количество попыток ввода OTP. Попробуйте позже.")

        # Проверка на истечение срока действия OTP
        if user.otp_expiry and timezone.now() > user.otp_expiry:
            raise serializers.ValidationError("OTP-код истек. Пожалуйста, запросите новый.")

        # Проверка правильности OTP
        if user.otp != otp:
            user.save()  # Сохранение в случае неверного OTP
            raise serializers.ValidationError("Неправильный OTP-код.")

        # Активация пользователя при успешной проверке
        user.is_active = True
        user.otp = None
        user.otp_expiry = None
        user.max_otp_try = settings.MAX_OTP_TRY
        user.save()

        return data

    def resend_otp(self, phone_number):
        """ Функция для повторной отправки OTP. """
        try:
            user = UserModel.objects.get(phone_number=phone_number)
        except UserModel.DoesNotExist:
            raise serializers.ValidationError("Пользователь с таким номером не найден.")

        otp = random.randint(1000, 9999)  # Генерация нового OTP
        otp_expiry = timezone.now() + timedelta(minutes=10)  # Время действия нового OTP

        user.otp = otp
        user.otp_expiry = otp_expiry
        user.max_otp_try = settings.MAX_OTP_TRY  # Сбросить количество попыток
        user.otp_max_out = None  # Сбросить блокировку по времени
        user.save()

        # Отправка OTP по SMS
        send_otp(user.phone_number, otp)
        return {"message": "OTP успешно отправлен снова."}


### 📌 **3. Сериализатор профиля пользователя**
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            "first_name",
            "last_name",
            "subscriptions"
        )


### 📌 **4. Полный сериализатор пользователя с профилем**
class UserFullProfileSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = UserModel
        fields = (
            "id",
            "phone_number",
            "email",
            "date_of_birth",
            "is_active",
            "profile"
        )
        read_only_fields = ("id", "is_active")

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", None)

        # Обновление данных пользователя
        instance.email = validated_data.get("email", instance.email)
        instance.date_of_birth = validated_data.get("date_of_birth", instance.date_of_birth)
        instance.save()

        # Обновление профиля пользователя
        if profile_data:
            profile = instance.profile
            profile.first_name = profile_data.get("first_name", profile.first_name)
            profile.last_name = profile_data.get("last_name", profile.last_name)
            profile.subscriptions = profile_data.get("subscriptions", profile.subscriptions)
            profile.save()

        return instance


class UserSerializer(serializers.ModelSerializer):
    # Use the 'profile' field which is the related name for UserProfile
    profile = UserProfileSerializer()

    class Meta:
        model = UserModel
        fields = '__all__'



from rest_framework_simplejwt.tokens import RefreshToken
class OTPAuthenticationSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        max_length=15,
        required=True,
        error_messages={"required": "Введите номер телефона."}
    )
    otp = serializers.CharField(
        max_length=4,  # Для 4-значного OTP
        required=True,
        error_messages={"required": "Введите OTP-код из SMS."}
    )

    def validate(self, data):
        phone_number = data.get("phone_number")
        otp = data.get("otp")

        phone_number = data.get("phone_number")
        otp = data.get("otp")

        try:
            user = UserModel.objects.get(phone_number=phone_number)
        except UserModel.DoesNotExist:
            raise serializers.ValidationError("Пользователь с таким номером не найден.")

        # Проверка на количество попыток
        if int(user.max_otp_try) <= 0:
            if user.otp_max_out and timezone.now() < user.otp_max_out:
                raise serializers.ValidationError("Превышено количество попыток ввода OTP. Попробуйте позже.")

        # Проверка правильности OTP
        if user.otp != otp:
            user.max_otp_try -= 1
            user.save()
            raise serializers.ValidationError("Неправильный OTP-код.")

        # Активация пользователя при успешной проверке
        user.is_active = True
        user.otp = None
        user.otp_expiry = None
        user.max_otp_try = settings.MAX_OTP_TRY  # Сбросить количество попыток
        user.save()

        # Генерация токенов
        refresh = RefreshToken.for_user(user)
        tokens = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        # Возвращаем токены
        return {
            "message": "Аутентификация прошла успешно.",
            "tokens": tokens,
        }

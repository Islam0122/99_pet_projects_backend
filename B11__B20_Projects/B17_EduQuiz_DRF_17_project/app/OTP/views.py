from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OTPSerializer
from .utils import send_otp_email

class SendOTPView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if email:
            try:
                send_otp_email(email)
                return Response({"message": "OTP был отправлен на ваш email."}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Email не был предоставлен."}, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = OTPSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "OTP подтвержден."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from ..models import GuestProfile, DriverProfile
from ..serializers import (
    GuestProfileSerializer,
    GuestProfileDetailSerializer,
    DriverProfileSerializer,
    DriverProfileDetailSerializer,
)
from ..permissions import IsOwnerOrReadOnly


class GuestProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return GuestProfileDetailSerializer
        return GuestProfileSerializer

    def get_queryset(self):
        return GuestProfile.objects.filter(user=self.request.user)

    def get_object(self):
        return get_object_or_404(GuestProfile, user=self.request.user)

    @extend_schema(
        description="Получить профиль текущего гостя"
    )
    def list(self, request, *args, **kwargs):
        try:
            profile = GuestProfile.objects.get(user=request.user)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except GuestProfile.DoesNotExist:
            return Response({
                'error': 'Профиль гостя не найден'
            }, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        description="Обновить профиль гостя"
    )
    def update(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Частично обновить профиль гостя"
    )
    def partial_update(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DriverProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return DriverProfileDetailSerializer
        return DriverProfileSerializer

    def get_queryset(self):
        """Пользователь видит только свой профиль"""
        return DriverProfile.objects.filter(user=self.request.user)

    def get_object(self):
        """Возвращаем профиль текущего пользователя"""
        return get_object_or_404(DriverProfile, user=self.request.user)

    @extend_schema(
        description="Получить профиль текущего водителя"
    )
    def list(self, request, *args, **kwargs):
        """Возвращаем только профиль текущего пользователя"""
        try:
            profile = DriverProfile.objects.get(user=request.user)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except DriverProfile.DoesNotExist:
            return Response({
                'error': 'Профиль водителя не найден'
            }, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        description="Обновить профиль водителя"
    )
    def update(self, request, *args, **kwargs):
        """Полное обновление профиля"""
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Частично обновить профиль водителя"
    )
    def partial_update(self, request, *args, **kwargs):
        """Частичное обновление профиля"""
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Получить статистику водителя"
    )
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Получение статистики водителя"""
        try:
            profile = DriverProfile.objects.get(user=request.user)
            return Response({
                'rating': profile.rating,
                'total_trips': profile.total_trips,
                'experience_years': profile.experience_years,
                'verified': profile.verified_driver,
            })
        except DriverProfile.DoesNotExist:
            return Response({
                'error': 'Профиль водителя не найден'
            }, status=status.HTTP_404_NOT_FOUND)


class MyProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="Получить профиль текущего пользователя (автоопределение типа)"
    )
    def get(self, request):
        user = request.user

        if user.role == 'guest':
            try:
                profile = GuestProfile.objects.get(user=user)
                serializer = GuestProfileDetailSerializer(profile)
                return Response({
                    'role': 'guest',
                    'profile': serializer.data
                })
            except GuestProfile.DoesNotExist:
                return Response({
                    'error': 'Профиль гостя не найден'
                }, status=status.HTTP_404_NOT_FOUND)

        elif user.role == 'driver':
            try:
                profile = DriverProfile.objects.get(user=user)
                serializer = DriverProfileDetailSerializer(profile)
                return Response({
                    'role': 'driver',
                    'profile': serializer.data
                })
            except DriverProfile.DoesNotExist:
                return Response({
                    'error': 'Профиль водителя не найден'
                }, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'error': 'Неизвестная роль пользователя'
        }, status=status.HTTP_400_BAD_REQUEST)
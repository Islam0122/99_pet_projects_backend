from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from ..models import Car, CarImage, DriverProfile
from ..serializers import (
    CarSerializer,
    CarDetailSerializer,
    CarCreateUpdateSerializer,
    CarImageSerializer,
    CarImageUploadSerializer
)
from ..permissions import IsDriver


class CarViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsDriver]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CarCreateUpdateSerializer
        if self.action in ['retrieve', 'list']:
            return CarDetailSerializer
        return CarSerializer

    def get_queryset(self):
        try:
            driver_profile = DriverProfile.objects.get(user=self.request.user)
            return Car.objects.filter(driver=driver_profile)
        except DriverProfile.DoesNotExist:
            return Car.objects.none()

    @extend_schema(
        description="Создать автомобиль водителя"
    )
    def create(self, request, *args, **kwargs):
        try:
            driver_profile = DriverProfile.objects.get(user=request.user)

            if Car.objects.filter(driver=driver_profile).exists():
                return Response({
                    'error': 'У водителя уже есть машина. Используйте UPDATE.'
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(driver=driver_profile)
                return Response(
                    CarDetailSerializer(serializer.instance).data,
                    status=status.HTTP_201_CREATED
                )

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except DriverProfile.DoesNotExist:
            return Response({
                'error': 'Только водители могут добавлять машины'
            }, status=status.HTTP_403_FORBIDDEN)

    @extend_schema(
        description="Обновить информацию об автомобиле"
    )
    def update(self, request, *args, **kwargs):
        try:
            driver_profile = DriverProfile.objects.get(user=request.user)
            car = get_object_or_404(Car, driver=driver_profile)

            serializer = self.get_serializer(car, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(CarDetailSerializer(serializer.instance).data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except DriverProfile.DoesNotExist:
            return Response({
                'error': 'Только водители могут обновлять машины'
            }, status=status.HTTP_403_FORBIDDEN)

    @extend_schema(
        description="Частично обновить информацию об автомобиле"
    )
    def partial_update(self, request, *args, **kwargs):
        try:
            driver_profile = DriverProfile.objects.get(user=request.user)
            car = get_object_or_404(Car, driver=driver_profile)

            serializer = self.get_serializer(car, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(CarDetailSerializer(serializer.instance).data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except DriverProfile.DoesNotExist:
            return Response({
                'error': 'Только водители могут обновлять машины'
            }, status=status.HTTP_403_FORBIDDEN)

    @extend_schema(
        description="Получить автомобиль водителя"
    )
    def list(self, request, *args, **kwargs):
        try:
            driver_profile = DriverProfile.objects.get(user=request.user)
            car = Car.objects.filter(driver=driver_profile).first()

            if car:
                serializer = CarDetailSerializer(car)
                return Response(serializer.data)

            return Response({
                'message': 'Машина не добавлена'
            }, status=status.HTTP_404_NOT_FOUND)

        except DriverProfile.DoesNotExist:
            return Response({
                'error': 'Только водители могут просматривать машины'
            }, status=status.HTTP_403_FORBIDDEN)

    @extend_schema(
        request=CarImageUploadSerializer,
        description="Загрузить изображение автомобиля"
    )
    @action(detail=False, methods=['post'])
    def upload_image(self, request):
        try:
            driver_profile = DriverProfile.objects.get(user=request.user)
            car = get_object_or_404(Car, driver=driver_profile)

            serializer = CarImageUploadSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            car_image = CarImage.objects.create(
                car=car,
                image=serializer.validated_data['image'],
                is_primary=serializer.validated_data.get('is_primary', False),
                order=serializer.validated_data.get('order', 0)
            )

            if car_image.is_primary:
                CarImage.objects.filter(car=car).exclude(id=car_image.id).update(is_primary=False)

            return Response(
                CarImageSerializer(car_image).data,
                status=status.HTTP_201_CREATED
            )

        except DriverProfile.DoesNotExist:
            return Response({
                'error': 'Только водители могут загружать изображения'
            }, status=status.HTTP_403_FORBIDDEN)

    @extend_schema(
        description="Удалить изображение автомобиля"
    )
    @action(detail=False, methods=['delete'], url_path='delete-image/(?P<image_id>[0-9]+)')
    def delete_image(self, request, image_id=None):
        try:
            driver_profile = DriverProfile.objects.get(user=request.user)
            car = get_object_or_404(Car, driver=driver_profile)
            car_image = get_object_or_404(CarImage, id=image_id, car=car)

            car_image.delete()

            return Response({
                'message': 'Изображение удалено'
            }, status=status.HTTP_200_OK)

        except DriverProfile.DoesNotExist:
            return Response({
                'error': 'Только водители могут удалять изображения'
            }, status=status.HTTP_403_FORBIDDEN)

    @extend_schema(
        description="Установить изображение как главное"
    )
    @action(detail=False, methods=['post'], url_path='set-primary-image/(?P<image_id>[0-9]+)')
    def set_primary_image(self, request, image_id=None):
        try:
            driver_profile = DriverProfile.objects.get(user=request.user)
            car = get_object_or_404(Car, driver=driver_profile)
            car_image = get_object_or_404(CarImage, id=image_id, car=car)

            car_image.set_as_primary()

            return Response({
                'message': 'Изображение установлено как главное'
            }, status=status.HTTP_200_OK)

        except DriverProfile.DoesNotExist:
            return Response({
                'error': 'Только водители могут устанавливать главное изображение'
            }, status=status.HTTP_403_FORBIDDEN)

    @extend_schema(
        description="Активировать автомобиль"
    )
    @action(detail=False, methods=['post'])
    def activate(self, request):
        """Активация автомобиля"""
        try:
            driver_profile = DriverProfile.objects.get(user=request.user)
            car = get_object_or_404(Car, driver=driver_profile)

            car.activate()

            return Response({
                'message': 'Автомобиль активирован'
            }, status=status.HTTP_200_OK)

        except DriverProfile.DoesNotExist:
            return Response({
                'error': 'Только водители могут активировать автомобили'
            }, status=status.HTTP_403_FORBIDDEN)

    @extend_schema(
        description="Деактивировать автомобиль"
    )
    @action(detail=False, methods=['post'])
    def deactivate(self, request):
        """Деактивация автомобиля"""
        try:
            driver_profile = DriverProfile.objects.get(user=request.user)
            car = get_object_or_404(Car, driver=driver_profile)

            car.deactivate()

            return Response({
                'message': 'Автомобиль деактивирован'
            }, status=status.HTTP_200_OK)

        except DriverProfile.DoesNotExist:
            return Response({
                'error': 'Только водители могут деактивировать автомобили'
            }, status=status.HTTP_403_FORBIDDEN)
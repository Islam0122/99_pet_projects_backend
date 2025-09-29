from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Reservation
from .serializers import ReservationSerializer

class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def cancel(self, request, pk=None):
        """
        PATCH /reservations/{id}/cancel/ - отмена бронирования
        """
        reservation = self.get_object()
        if reservation.status == 'cancelled':
            return Response({"detail": "Бронирование уже отменено"}, status=status.HTTP_400_BAD_REQUEST)
        reservation.status = 'cancelled'
        reservation.save()
        return Response({"detail": "Бронирование отменено"}, status=status.HTTP_200_OK)

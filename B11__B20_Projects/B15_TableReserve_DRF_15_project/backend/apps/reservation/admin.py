from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'table', 'date', 'start_time', 'end_time', 'status', 'created_at')
    list_filter = ('status', 'table', 'date')
    search_fields = ('user__username', 'user__email', 'table__number')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-date', 'start_time')
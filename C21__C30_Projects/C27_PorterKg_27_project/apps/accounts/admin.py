from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, GuestProfile, DriverProfile, Car, CarImage
from django.contrib.auth.models import Group
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = [
        'email',
        'full_name',
        'role',
        'is_verified_badge',
        'auth_type',
        'is_active_badge',
        'created_at'
    ]
    list_filter = [
        'role',
        'is_verified',
        'auth_type',
        'is_active',
        'is_staff',
        'created_at'
    ]
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'

    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Основная информация', {
            'fields': ('email', 'password')
        }),
        ('Личные данные', {
            'fields': ('first_name', 'last_name')
        }),
        ('Статус и роль', {
            'fields': ('role', 'is_verified', 'auth_type')
        }),
        ('Права доступа', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            ),
            'classes': ('collapse',)
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'first_name',
                'last_name',
                'password1',
                'password2',
                'role',
                'auth_type'
            ),
        }),
    )

    def is_verified_badge(self, obj):
        if obj.is_verified:
            return format_html(
                '<span style="color: green;">✓ Подтвержден</span>'
            )
        return format_html(
            '<span style="color: red;">✗ Не подтвержден</span>'
        )

    is_verified_badge.short_description = 'Email'

    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="color: green;">✓ Активен</span>'
            )
        return format_html(
            '<span style="color: red;">✗ Неактивен</span>'
        )

    is_active_badge.short_description = 'Статус'


@admin.register(GuestProfile)
class GuestProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user_email',
        'user_full_name',
        'phone_number',
        'has_avatar',
        'created_at'
    ]
    search_fields = [
        'user__email',
        'user__first_name',
        'user__last_name',
        'phone_number'
    ]
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Пользователь', {
            'fields': ('user',)
        }),
        ('Контактная информация', {
            'fields': ('phone_number',)
        }),
        ('Дополнительная информация', {
            'fields': ('avatar', 'bio', 'birth_date')
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = 'Email'
    user_email.admin_order_field = 'user__email'

    def user_full_name(self, obj):
        return obj.user.full_name

    user_full_name.short_description = 'Полное имя'

    def has_avatar(self, obj):
        if obj.avatar:
            return format_html('<span style="color: green;">✓</span>')
        return format_html('<span style="color: red;">✗</span>')

    has_avatar.short_description = 'Аватар'


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1
    readonly_fields = ['created_at']
    fields = ['image', 'is_primary', 'order', 'created_at']


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = [
        'full_name',
        'driver_name',
        'number_plate',
        'year',
        'color',
        'fuel_type',
        'is_active_badge',
        'has_images_badge'
    ]
    search_fields = [
        'driver__user__email',
        'marka',
        'model',
        'number_plate',
        'vin_code'
    ]
    list_filter = [
        'fuel_type',
        'year',
        'is_active',
        'created_at'
    ]
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    inlines = [CarImageInline]

    fieldsets = (
        ('Водитель', {
            'fields': ('driver',)
        }),
        ('Основная информация', {
            'fields': ('marka', 'model', 'color', 'year')
        }),
        ('Регистрационные данные', {
            'fields': ('number_plate', 'vin_code')
        }),
        ('Технические характеристики', {
            'fields': ('fuel_type', 'max_passengers')
        }),
        ('Дополнительно', {
            'fields': ('description', 'is_active')
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def driver_name(self, obj):
        return obj.driver.user.full_name

    driver_name.short_description = 'Водитель'
    driver_name.admin_order_field = 'driver__user__first_name'

    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green;">✓ Активен</span>')
        return format_html('<span style="color: red;">✗ Неактивен</span>')

    is_active_badge.short_description = 'Статус'

    def has_images_badge(self, obj):
        count = obj.images.count()
        if count > 0:
            return format_html(
                '<span style="color: green;">✓ ({} шт.)</span>',
                count
            )
        return format_html('<span style="color: red;">✗ Нет</span>')

    has_images_badge.short_description = 'Фото'


@admin.register(DriverProfile)
class DriverProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user_full_name',
        'phone_number',
        'rating',
        'total_trips',
        'experience_years',
        'verified_badge',
        'has_car_badge'
    ]
    search_fields = [
        'user__email',
        'user__first_name',
        'user__last_name',
        'phone_number',
        'driver_license_number'
    ]
    list_filter = [
        'verified_driver',
        'experience_years',
        'created_at'
    ]
    readonly_fields = ['created_at', 'updated_at', 'rating']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Пользователь', {
            'fields': ('user',)
        }),
        ('Контактная информация', {
            'fields': ('phone_number', 'bio')
        }),
        ('Водительские данные', {
            'fields': (
                'driver_license_number',
                'driver_license_category',
                'driver_license_expiry',
                'experience_years'
            )
        }),
        ('Статистика', {
            'fields': ('rating', 'total_trips', 'verified_driver')
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = 'Email'
    user_email.admin_order_field = 'user__email'

    def user_full_name(self, obj):
        return obj.user.full_name

    user_full_name.short_description = 'Полное имя'

    def rating_display(self, obj):
        rating = float(obj.rating) | 0.0
        if rating >= 90:
            color = 'green'
        elif rating >= 70:
            color = 'orange'
        else:
            color = 'red'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{:.1f}</span>',
            color,
            rating
        )

    rating_display.short_description = 'Рейтинг'
    rating_display.admin_order_field = 'rating'

    def verified_badge(self, obj):
        if obj.verified_driver:
            return format_html('<span style="color: green;">✓ Верифицирован</span>')
        return format_html('<span style="color: orange;">⏳ Не верифицирован</span>')

    verified_badge.short_description = 'Верификация'

    def has_car_badge(self, obj):
        if hasattr(obj, 'car'):
            return format_html('<span style="color: green;">✓ Есть</span>')
        return format_html('<span style="color: red;">✗ Нет</span>')

    has_car_badge.short_description = 'Автомобиль'


@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'car_info',
        'image_preview',
        'is_primary_badge',
        'order',
        'created_at'
    ]
    list_filter = ['is_primary', 'created_at']
    readonly_fields = ['created_at', 'image_preview']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Основная информация', {
            'fields': ('car', 'image', 'image_preview')
        }),
        ('Настройки отображения', {
            'fields': ('is_primary', 'order')
        }),
        ('Временные метки', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def car_info(self, obj):
        return str(obj.car)

    car_info.short_description = 'Автомобиль'

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 200px;" />',
                obj.image.url
            )
        return '-'

    image_preview.short_description = 'Превью'

    def is_primary_badge(self, obj):
        if obj.is_primary:
            return format_html('<span style="color: green;">✓ Главное</span>')
        return format_html('<span style="color: gray;">-</span>')

    is_primary_badge.short_description = 'Тип'

admin.site.unregister(Group)
admin.site.unregister(OutstandingToken)
admin.site.unregister(BlacklistedToken)

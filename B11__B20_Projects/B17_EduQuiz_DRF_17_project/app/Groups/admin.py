from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Group, Student

class StudentInline(admin.TabularInline):
    model = Student
    extra = 1
    fields = ('full_name', 'group', 'is_active', 'created_by', 'updated_user')
    readonly_fields = ('created_at', 'updated_at')

class GroupAdmin(SimpleHistoryAdmin, admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at', 'created_by')
    list_filter = ('created_at', 'created_by')
    search_fields = ('name',)
    ordering = ('-created_at',)
    fieldsets = (
        (None, {
            'fields': ('name', 'created_by', 'updated_user')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_user')
    inlines = [StudentInline]

    def save_model(self, request, obj, form, change):
        """Автоматически устанавливаем create_user и updated_user"""
        if not obj.pk:  # Если запись создаётся впервые
            obj.create_user = request.user
        obj.updated_user = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Group, GroupAdmin)

class StudentAdmin(SimpleHistoryAdmin, admin.ModelAdmin):
    list_display = ('full_name', 'group', 'is_active', 'created_at', 'updated_at', 'created_by', 'updated_user')
    list_filter = ('group', 'is_active', 'created_by')
    search_fields = ('full_name',)
    ordering = ('-created_at',)

    fieldsets = (
        (None, {
            'fields': ('full_name', 'group', 'is_active', 'created_by', 'updated_user')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_user')


    def save_model(self, request, obj, form, change):
        """Автоматически устанавливаем create_user и updated_user"""
        if not obj.pk:  # Если запись создаётся впервые
            obj.created_by = request.user
        obj.updated_user = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Student, StudentAdmin)


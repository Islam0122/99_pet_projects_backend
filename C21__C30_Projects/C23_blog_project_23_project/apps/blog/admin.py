from django.contrib import admin
from .models import  Article, Comment


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'content', 'author__username')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'article', 'author', 'content', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'author__username', 'article__title')
    readonly_fields = ('created_at', 'updated_at')

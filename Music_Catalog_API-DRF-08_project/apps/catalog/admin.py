from django.contrib import admin
from .models import Artist, Album, Song, AlbumSong


class AlbumSongInline(admin.TabularInline):
    model = AlbumSong
    extra = 1
    autocomplete_fields = ['song']
    fields = ('track_number', 'song')
    ordering = ('track_number',)


class AlbumInline(admin.TabularInline):
    model = Album
    extra = 1
    fields = ('title', 'release_year')
    show_change_link = True


class SongInline(admin.TabularInline):
    model = Song
    extra = 1
    fields = ('title', 'duration')
    show_change_link = True


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'created_at')
    search_fields = ('name', 'country')
    inlines = [AlbumInline, SongInline]


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'release_year', 'created_at')
    search_fields = ('title', 'artist__name')
    list_filter = ('release_year', 'artist')
    inlines = [AlbumSongInline]


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'duration', 'created_at')
    search_fields = ('title', 'artist__name')
    list_filter = ('artist',)


@admin.register(AlbumSong)
class AlbumSongAdmin(admin.ModelAdmin):
    list_display = ('track_number', 'album', 'song')
    list_filter = ('album',)
    search_fields = ('song__title', 'album__title')

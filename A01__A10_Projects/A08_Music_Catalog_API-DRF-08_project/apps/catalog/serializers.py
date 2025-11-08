from rest_framework import serializers
from .models import Artist, Album, Song, AlbumSong


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ["id", "title", "duration", "artist", "created_at", "updated_at"]


class AlbumSongSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumSong
        fields = ['id', 'album', 'song', 'track_number']


class AlbumSerializer(serializers.ModelSerializer):
    artist_name = serializers.CharField(source="artist.name", read_only=True)
    album_songs = AlbumSongSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = [
            "id",
            "title",
            "artist",
            "artist_name",
            "release_year",
            "description",
            "album_songs",
            "created_at",
            "updated_at",
        ]


class ArtistSerializer(serializers.ModelSerializer):
    albums = AlbumSerializer(many=True, read_only=True)
    songs = SongSerializer(many=True, read_only=True)

    class Meta:
        model = Artist
        fields = [
            "id",
            "name",
            "bio",
            "country",
            "albums",
            "songs",
            "created_at",
            "updated_at",
        ]

from rest_framework import viewsets
from .models import Artist, Album, Song, AlbumSong
from .serializers import ArtistSerializer, AlbumSerializer, SongSerializer, AlbumSongSerializer


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all().order_by("name")
    serializer_class = ArtistSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all().order_by("-release_year", "title")
    serializer_class = AlbumSerializer


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all().order_by("title")
    serializer_class = SongSerializer


class AlbumSongViewSet(viewsets.ModelViewSet):
    queryset = AlbumSong.objects.all().order_by("track_number")
    serializer_class = AlbumSongSerializer

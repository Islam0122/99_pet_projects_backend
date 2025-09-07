from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.management import call_command
from .models import Artist, Album, Song, AlbumSong


@receiver(post_migrate)
def load_data(sender, **kwargs):
    if not Artist.objects.exists():
        call_command('loaddata', 'apps/catalog/fixtures/initial_artist_data.json')
    if not Album.objects.exists():
        call_command('loaddata', 'apps/catalog/fixtures/initial_album_data.json')
    if not Song.objects.exists():
        call_command('loaddata', 'apps/catalog/fixtures/initial_song_data.json')
    if not AlbumSong.objects.exists():
        call_command('loaddata', 'apps/catalog/fixtures/initial_album_song_data.json')

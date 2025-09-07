from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.catalog.models import Artist, Album, Song, AlbumSong


class ArtistTests(APITestCase):
    def setUp(self):
        Artist.objects.all().delete()
        self.artist = Artist.objects.create(name="Michael Jackson", country="USA")

    def test_create_artist(self):
        url = reverse("artist-list")
        data = {"name": "Eminem", "country": "USA"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_artists(self):
        url = reverse("artist-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_artist(self):
        url = reverse("artist-detail", args=[self.artist.id])
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_artist(self):
        url = reverse("artist-detail", args=[self.artist.id])
        data = {"name": "MJ", "country": "USA"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.artist.refresh_from_db()
        self.assertEqual(self.artist.name, "MJ")

    def test_delete_artist(self):
        url = reverse("artist-detail", args=[self.artist.id])
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class AlbumTests(APITestCase):
    def setUp(self):
        Artist.objects.all().delete()
        Album.objects.all().delete()
        self.artist = Artist.objects.create(name="Queen Test", country="UK")
        self.album = Album.objects.create(title="Greatest Hits Test", artist=self.artist, release_year=1981)

    def test_create_album(self):
        url = reverse("album-list")
        data = {"title": "News of the World Test", "artist": self.artist.id, "release_year": 1977}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_albums(self):
        url = reverse("album-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_retrieve_album(self):
        url = reverse("album-detail", args=[self.album.id])
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.album.title)

    def test_update_album(self):
        url = reverse("album-detail", args=[self.album.id])
        data = {"title": "Greatest Hits (Remastered Test)", "artist": self.artist.id, "release_year": 1981}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.album.refresh_from_db()
        self.assertEqual(self.album.title, "Greatest Hits (Remastered Test)")

    def test_delete_album(self):
        url = reverse("album-detail", args=[self.album.id])
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Album.objects.filter(id=self.album.id).exists())


class SongTests(APITestCase):
    def setUp(self):
        Artist.objects.all().delete()
        Song.objects.all().delete()
        self.artist = Artist.objects.create(name="The Beatles Test", country="UK")
        self.song = Song.objects.create(title="Yesterday Test", duration=123, artist=self.artist)

    def test_create_song(self):
        url = reverse("song-list")
        data = {"title": "Hey Jude Test", "duration": 431, "artist": self.artist.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Hey Jude Test")

    def test_list_songs(self):
        url = reverse("song-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_retrieve_song(self):
        url = reverse("song-detail", args=[self.song.id])
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.song.title)

    def test_update_song(self):
        url = reverse("song-detail", args=[self.song.id])
        data = {"title": "Yesterday (Remastered Test)", "duration": 125, "artist": self.artist.id}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.song.refresh_from_db()
        self.assertEqual(self.song.title, "Yesterday (Remastered Test)")
        self.assertEqual(self.song.duration, 125)

    def test_delete_song(self):
        url = reverse("song-detail", args=[self.song.id])
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Song.objects.filter(id=self.song.id).exists())


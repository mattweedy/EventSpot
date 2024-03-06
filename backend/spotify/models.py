from django.apps import apps
from django.db import models
from backend.spotify.spotify_auth import get_artist_genres
from django.core.exceptions import ObjectDoesNotExist

class Track(models.Model):
    class Meta:
        app_label = "backend"

    name = models.CharField(max_length=200)
    spotify_id = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    artist_id = models.CharField(max_length=200)
    genres = models.CharField(max_length=200)
    popularity = models.IntegerField()

    def create_track_from_spotify(cls, track):
        name = track['name']
        spotify_id = track['id']
        artist = track['artists'][0]['name']
        artist_id = track['artists'][0]['id']
        popularity = track['popularity']

        # for genres, pull genres from artist
        try:
            artist_obj = Artist.objects.get(spotify_id=artist_id)
            if artist_obj.genres:
                genres = artist_obj.genres
            else:
                genres = get_artist_genres(artist_id=artist_id)
                artist_obj.genres = genres
                artist_obj.save()
        except ObjectDoesNotExist:
            genres = get_artist_genres(artist_id=artist_id)
            Artist.objects.create(name=artist, spotify_id=artist_id, genres=genres, popularity=popularity or 0)

        defaults={
            'name': name,
            'artist': artist,
            'artist_id': artist_id,
            'genres': genres,
            'popularity': popularity,
        }

        try:
            track_obj = cls.objects.get(spotify_id=spotify_id)
            for key, value in defaults.items():
                if getattr(track_obj, key) != value:
                    setattr(track_obj, key, value)
            track_obj.save()
            print("An existing track was updated.")
        except cls.DoesNotExist:
            track_obj = cls.objects.create(spotify_id=spotify_id, **defaults)
            print("A new track was created.")

        return track_obj

    def __str__(self):
        return (
            f"------------------------\n"
            f"TRACK      : {self.name}\n"
            f"ID         : {self.spotify_id}\n"
            f"ARTIST     : {self.artist}\n"
            f"GENRES     : {self.genres}\n"
            f"POPULARITY : {self.popularity}"
            f"\n------------------------"
        )
    
    
class Artist(models.Model):
    class Meta:
        app_label = "backend"

    name = models.CharField(max_length=200)
    spotify_id = models.CharField(max_length=200)
    genres = models.CharField(max_length=200)
    link = models.CharField(max_length=200)
    popularity = models.IntegerField()

    def create_artist_from_spotify(cls, artist):
        # check that the artist dictionary contains all the necessary keys
        required_keys = ['id', 'name', 'genres', 'external_urls', 'popularity']
        for key in required_keys:
            if key not in artist:
                raise ValueError(f"Key '{key}' not found in artist dictionary")

        # check that the 'external_urls' dictionary contains the 'spotify' key
        if 'spotify' not in artist['external_urls']:
            raise ValueError("'spotify' key not found in 'external_urls' dictionary")

        artist_obj, created = cls.objects.filter(spotify_id=artist['id']).first(), True
        if not artist_obj:
            artist_obj = cls(
                spotify_id=artist['id'], 
                name=artist['name'], 
                genres=artist['genres'], 
                link=artist['external_urls']['spotify'], 
                popularity=artist['popularity'] or 0
            )
            artist_obj.save()
        return artist_obj

    def to_dict(self):
        return (
            f"------------------------\n"
            f"ARTIST     : {self.name}\n"
            f"ID         : {self.spotify_id}\n"
            f"GENRES     : {self.genres}\n"
            f"LINK       : {self.link}\n"
            f"POPULARITY : {self.popularity}"
            f"\n------------------------"
        )

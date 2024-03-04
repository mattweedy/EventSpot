from django.apps import apps
from django.db import models
from spotify.spotify_auth import get_artist_genres
from django.core.exceptions import ObjectDoesNotExist

class Track(models.Model):
    class Meta:
        app_label = "spotify"

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
        app_label = "spotify"

    name = models.CharField(max_length=200)
    spotify_id = models.CharField(max_length=200)
    genres = models.CharField(max_length=200)
    link = models.CharField(max_length=200)
    popularity = models.IntegerField()

    def create_artist_from_spotify(cls, artist):
        name = artist["name"]
        spotify_id = artist["id"]
        try:
            genres = artist["genres"]
        except KeyError:
            genres = "N/A"
        link = artist["external_urls"]["spotify"]
        popularity = artist["popularity"]

        artist_obj, created = cls.objects.update_or_create(
            spotify_id=artist["id"],
            defaults={
                'name': name,
                'spotify_id': spotify_id,
                'genres': genres,
                'link': link,
                'popularity': popularity,
            },
        )
        if created:
            print("A new artist was created.")
        else:
            print("An existing artist was updated.")

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

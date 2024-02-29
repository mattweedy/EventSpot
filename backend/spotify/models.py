from django.db import models
from spotify.spotify_auth import get_artist_genres

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
        genres_list = get_artist_genres(artist_id=artist_id)
        genres = genres_list


        track_insert, created = cls.objects.update_or_create(
            spotify_id=track['id'],
            defaults={
                'name': name,
                'spotify_id': spotify_id,
                'artist': artist,
                'artist_id': artist_id,
                'genres': genres,
                'popularity': popularity,
            },
        )
        if created:
            print("A new track was created.")
        else:
            print("An existing track was updated.")

        return track_insert


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
        name = artist["name"]
        spotify_id = artist["id"]
        try:
            genres = artist["genres"]
        except KeyError:
            genres = "N/A"
        link = artist["external_urls"]["spotify"]
        popularity = artist["popularity"]

        artist_insert, created = cls.objects.update_or_create(
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

        return artist_insert

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

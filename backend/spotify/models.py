from django.db import models
from backend import utils
from backend.spotify.spotify_auth import get_artist_genres
from django.core.exceptions import ObjectDoesNotExist

class Track(models.Model):
    class Meta:
        app_label = "backend"

    name = models.CharField(max_length=500)
    spotify_id = models.CharField(max_length=500)
    artist = models.CharField(max_length=500)
    artist_id = models.CharField(max_length=500)
    genres = models.CharField(max_length=500)
    popularity = models.IntegerField()
    users = models.CharField(max_length=250, default="")

    def create_track_from_spotify(cls, track, user):
        name = track['name']
        spotify_id = track['id']
        artist = track['artists'][0]['name']
        artist_id = track['artists'][0]['id']
        popularity = track['popularity']

        link = ""
        # for genres, pull genres from artist
        try:
            # check if artist exists in the database
            artist_obj = Artist.objects.filter(spotify_id=artist_id).first()
            if artist_obj:
                # if the artist has genres, return them
                if artist_obj.genres:
                    genres = artist_obj.genres
                # if the artist doesn't have genres, fetch them from Spotify API
                else:
                    genres, link = get_artist_genres(artist_id=artist_id)
                    artist_obj.genres = genres
                    artist_obj.link = link
                    artist_obj.users += user + ","
                    artist_obj.save()
            # if the artist doesn't exist in the database, continue to fetch genres from Spotify API
            else:
                genres, link = get_artist_genres(artist_id=artist_id)
                Artist.objects.create(name=artist, spotify_id=artist_id, genres=genres, link=link, popularity=popularity or 0, users=user)
        except ObjectDoesNotExist:
            genres, link = get_artist_genres(artist_id=artist_id)
            Artist.objects.create(name=artist, spotify_id=artist_id, genres=genres, link=link, popularity=popularity or 0, users=user)

        defaults={
            'name': name,
            'artist': artist,
            'artist_id': artist_id,
            'genres': genres,
            'popularity': popularity,
        }

        # create or update the Track
        try:
            # check if track exists in the database
            track_obj = cls.objects.get(spotify_id=spotify_id)
            updated = False
            for key, value in defaults.items():
                # update the track if any of the fields have changed
                if getattr(track_obj, key) != value:
                    setattr(track_obj, key, value)
                    updated = True
            if updated:
                track_obj.save()
                print("An existing track was updated.")
            else:
                # print("An existing track was found.")
                pass
        except cls.DoesNotExist:
            # create a new track if it doesn't exist
            track_obj = cls.objects.create(spotify_id=spotify_id, **defaults)
            print("A new track was created.")

        # attatch the user who added the track
        if utils.get_access_token():
            if user not in track_obj.users:
                track_obj.users += user + ","
                track_obj.save()

        return track_obj

    def __str__(self):
        return (
            f"------------------------\n"
            f"TRACK      : {self.name}\n"
            f"ID         : {self.spotify_id}\n"
            f"ARTIST     : {self.artist}\n"
            f"GENRES     : {self.genres}\n"
            f"POPULARITY : {self.popularity}\n"
            f"USERS      : {self.users}"
            f"\n------------------------"
        )
    
    
class Artist(models.Model):
    class Meta:
        app_label = "backend"

    name = models.CharField(max_length=500)
    spotify_id = models.CharField(max_length=500)
    genres = models.CharField(max_length=500)
    link = models.CharField(max_length=500)
    popularity = models.IntegerField()
    users = models.CharField(max_length=250, default="")

    def create_artist_from_spotify(cls, artist, user):
        # check that the artist dictionary contains all the necessary keys
        required_keys = ['id', 'name', 'genres', 'external_urls', 'popularity']
        for key in required_keys:
            if key not in artist:
                raise ValueError(f"Key '{key}' not found in artist dictionary")

        # check that the 'external_urls' dictionary contains the 'spotify' key
        if 'spotify' not in artist['external_urls']:
            raise ValueError("'spotify' key not found in 'external_urls' dictionary")

        artist_obj = cls.objects.filter(spotify_id=artist['id']).first()
        if artist_obj:
            # print("An existing artist was found.")
            # update the artist spotify link
            artist_obj.link = artist['external_urls']['spotify']
            artist_obj.save()
        else:
            artist_obj = cls(
                spotify_id=artist['id'], 
                name=artist['name'], 
                genres=artist['genres'], 
                link=artist['external_urls']['spotify'], 
                popularity=artist['popularity'] or 0
            )
            artist_obj.save()
            print("A new artist was created.")

        # always set the link field
        artist_obj.link = artist['external_urls']['spotify']

        # always add the user to the users field if the user is not already in it
        if user not in artist_obj.users:
            artist_obj.users += user + ","

        artist_obj.save()

        return artist_obj

    # def create_artist_from_spotify(cls, artist, user):
    #     # check that the artist dictionary contains all the necessary keys
    #     required_keys = ['id', 'name', 'genres', 'external_urls', 'popularity']
    #     for key in required_keys:
    #         if key not in artist:
    #             raise ValueError(f"Key '{key}' not found in artist dictionary")

    #     # check that the 'external_urls' dictionary contains the 'spotify' key
    #     if 'spotify' not in artist['external_urls']:
    #         raise ValueError("'spotify' key not found in 'external_urls' dictionary")

    #     artist_obj = cls.objects.filter(spotify_id=artist['id']).first()
    #     if artist_obj:
    #         # print("An existing artist was found.")
    #         pass
    #     else:
    #         artist_obj = cls(
    #             spotify_id=artist['id'], 
    #             name=artist['name'], 
    #             genres=artist['genres'], 
    #             link=artist['external_urls']['spotify'], 
    #             popularity=artist['popularity'] or 0
    #         )
    #         artist_obj.save()
    #         print("A new artist was created.")

    #     if utils.get_access_token():
    #         if user not in artist_obj.users:
    #             artist_obj.users += user + ","
    #             artist_obj.save()

    #     return artist_obj


    def __str__(self):
        return (
            f"------------------------\n"
            f"ARTIST     : {self.name}\n"
            f"ID         : {self.spotify_id}\n"
            f"GENRES     : {self.genres}\n"
            f"LINK       : {self.link}\n"
            f"POPULARITY : {self.popularity}\n"
            f"USERS      : {self.users}"
            f"\n------------------------"
        )

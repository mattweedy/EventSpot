import utils
from django.http import JsonResponse
from django.core.cache import cache
from datetime import datetime, timedelta
from django.shortcuts import redirect
from django.contrib.auth import logout
from .spotify_auth import get_user_profile, get_user_top_items
from spotify.models import Track, Artist

genre_dict = {
    "techno": ["techno", "electronic", "edm", "dance"],
    "house": ["house", "electronic", "edm", "dance"],
    "trance": ["trance", "electronic", "edm", "dance"],
    "dubstep": ["dubstep", "electronic", "edm", "dance"],
    "drum and bass": ["drum and bass", "electronic", "edm", "dance"],
    "gabber": ["gabber", "electronic", "edm", "dance"],
    "hardgroove": ["hardgroove", "electronic", "dance", "techno"],
    "hardstyle": ["hardstyle", "electronic", "edm", "dance", "techno"],
    "psytrance": ["psytrance", "electronic", "edm", "dance", "trance"],
    "synthpop": ["synthpop", "grunge", "alternative", "indie"],
    "trap": ["trap", "rap", "hip hop", "street"],
    "hip hop": ["hip hop", "rap", "street"],
    "hiphop": ["hip hop", "rap", "street"],
    "rap": ["rap", "hip hop", "street"],
    "pop": ["pop", "dance"],
    "dance": ["pop", "dance"],
    "rock": ["rock", "metal"],
    "metal": ["rock", "metal", "hard rock"],
    "hard rock": ["rock", "metal", "hard rock"],
    "country": ["country", "bluegrass"],
    "bluegrass": ["country", "bluegrass"],
    "jazz": ["jazz", "blues"],
    "blues": ["jazz", "blues"],
    "classical": ["classical", "orchestral"],
    "orchestral": ["classical", "orchestral"],
    "electronic": ["electronic", "edm", "dance"],
    "edm": ["electronic", "edm", "dance"],
    "indie": ["indie", "alternative"],
    "alternative": ["indie", "alternative"],
    "folk": ["folk", "acoustic"],
    "acoustic": ["folk", "acoustic"],
    "r&b": ["r&b", "soul"],
    "soul": ["r&b", "soul"],
    "reggae": ["reggae", "ska"],
    "ska": ["reggae", "ska"],
    "punk": ["punk", "emo"],
    "emo": ["punk", "emo"],
    "latin": ["latin", "salsa"],
    "salsa": ["latin", "salsa"],
    "gospel": ["gospel", "spiritual"],
    "spiritual": ["gospel", "spiritual"],
    "funk": ["funk", "disco"],
    "disco": ["funk", "disco"],
    "world": ["world", "international"],
    "international": ["world", "international"],
    "new age": ["new age", "ambient"],
    "ambient": ["new age", "ambient"],
    "soundtrack": ["soundtrack", "score"],
    "score": ["soundtrack", "score"],
    "comedy": ["comedy", "parody"],
    "parody": ["comedy", "parody"],
    "spoken word": ["spoken word", "audiobook"],
    "audiobook": ["spoken word", "audiobook"],
    "children's": ["children's", "kids"],
    "kids": ["children's", "kids"],
    "holiday": ["holiday", "christmas"],
    "christmas": ["holiday", "christmas"],
    "easy listening": ["easy listening", "mood"],
    "mood": ["easy listening", "mood"],
    "brazilian": ["brazilian", "samba"],
    "samba": ["brazilian", "samba"],
    "fado": ["fado", "portuguese"],
    "portuguese": ["fado", "portuguese"],
    "tango": ["tango", "argentinian"],
}


def add_genres(genre_list):
    """
    Add more genres to the genre list.
    """
    new_genre_list = genre_list.copy()
    for genre, add_genres in genre_dict.items():
        for existing_genre in new_genre_list:
            if genre in existing_genre:
                for add_genre in add_genres:
                    if add_genre not in new_genre_list:
                        new_genre_list.append(add_genre)
    return new_genre_list


# LOGIN AND LOGUT VIEWS --------------------------------------------------------
def check_logged_in(request):
    """
    Check if the user is logged in.
    """
    try:
        access_token = utils.get_access_token()
    except Exception as e:
        print(f"An error occurred during the get_access_token process: {e}")
        return JsonResponse({"isLoggedIn": False})

    if access_token is None:
        return JsonResponse({"isLoggedIn": False})
    else:
        return JsonResponse({"isLoggedIn": True, "accessToken": access_token})
    

def logout_view(request):
    """
    Log the user out.
    """
    logout(request)
    cache.delete('spotify_access_token')
    cache.delete('spotify_refresh_token')
    cache.delete('oauth_state')
    cache.delete('code_verifier')
    return redirect('http://localhost:3000')
# END LOGIN AND LOGOUT VIEWS ----------------------------------------------------

# DATA VIEWS -------------------------------------------------------------
def user_profile(request):
    """
    Get the user's profile information.
    """
    return get_user_profile(request)


def top_tracks(request):
    """
    Get the user's top tracks.
    """
    try:
        access_token = utils.get_access_token()
    except Exception as e:
        return JsonResponse({"TOKEN ERROR : Couldn't retrieve access token": str(e)})

    try:
        top_tracks = get_user_top_items(access_token, 'tracks', 20)
        # return JsonResponse(top_tracks, safe=False)

        if 'items' in top_tracks:
            tracks = top_tracks["items"]

            for track in tracks:
                try:
                    new_track = Track.create_track_from_spotify(cls=Track, track=track)
                    print(new_track)
                except Exception as e:
                    print("An error occurred while creating track object")
                    print(e)
        else:
            print("No items found in top_tracks")
            return JsonResponse({"error": "No items found in top_tracks"})

        return JsonResponse(top_tracks, safe=False)
    
    except Exception as e:
        return JsonResponse({"error": str(e)})


def top_artists(request):
    """
    Get the user's top artists.
    """
    try:
        access_token = utils.get_access_token()
    except Exception as e:
        return JsonResponse({"TOKEN ERROR : Couldn't retrieve access token": str(e)})
    
    try:
        top_artists = get_user_top_items(access_token, 'artists', 20)

        if 'items' in top_artists:
            artists = top_artists["items"]

            for artist in artists:
                try:
                    # add genres to the artist
                    artist['genres'] = add_genres(artist['genres'])
                    new_artist = Artist.create_artist_from_spotify(cls=Artist, artist=artist)
                    print(new_artist)

                    # convert the Artist object to a dictionary
                    artist_dict = new_artist.__dict__

                    # remove any non-serializable attributes
                    artist_dict = {k: v for k, v in artist_dict.items() if not callable(v)}

                except Exception as e:
                    print("An error occurred while creating artist object")
                    print(e)
        else:
            print("No items found in top_artists")
            return JsonResponse({"error": "No items found in top_artists"})

        return JsonResponse(top_artists.items, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)})
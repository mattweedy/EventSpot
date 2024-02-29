import json
import utils
import base64
import string
import hashlib
import secrets
import requests
from django.apps import apps
from django.conf import settings
from django.core.cache import cache
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta
from requests_oauthlib import OAuth2Session
from requests.exceptions import RequestException


client_id = settings.SPOTIFY_CLIENT_ID
client_secret = settings.SPOTIFY_CLIENT_SECRET
redirect_uri = settings.SPOTIFY_REDIRECT_URI
scope = 'user-read-private user-read-email user-top-read'
authUrl = 'https://accounts.spotify.com/authorize'


def generate_code_verifier(length=128):
    """
    Generate a code verifier for PKCE.
    """
    allowed_chars = string.ascii_letters + string.digits + '-._~' # create string of all allowed characters

    # randomly select characters from allowed_chars and join them together
    # to create a code verifier of the specified length
    return ''.join(secrets.choice(allowed_chars) for _ in range(length))


def start_auth(request):
    """
    Start authentication process and redirect user to Spotify's authorization page.
    """
    try:
        spotify = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)

        # generate a code verifier
        code_verifier = generate_code_verifier()

        # generate a code challenge
        # hash verifier with sha256 and url-safe base64 encode the result
        # decoded to a utf-8 string
        code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode('utf-8')).digest()).decode('utf-8').rstrip('=')

        # redirect user to Spotify authorization apge
        authorization_url, state = spotify.authorization_url(
            'https://accounts.spotify.com/authorize',
            code_challenge_method='S256',
            code_challenge=code_challenge,
        )

        # store the state and code_verifier in the session and cache to protect against CSRF
        # request.session['oauth_state'] = state
        # request.session['code_verifier'] = code_verifier
       
        cache.set('oauth_state', state, 60*5)
        cache.set('code_verifier', code_verifier, 60*5)

        return redirect(authorization_url)
    except Exception as e:
        print(f"An error occurred during the start_auth process: {e}")
        return HttpResponse(status=500)


def spotify_callback(request):
    """
    Callback for Spotify's authorization page.
    """
    try:
        # call get_spotify_access_token to get the access token
        
        get_spotify_access_token(request)

        return redirect('http://localhost:3000')
    except RequestException as e:
        print(f"An error occurred during the spotify_callback process: {e}")
        return HttpResponse(status=500)
    except KeyError:
        print("Code verifier not found in session.")
        return HttpResponse(status=500)


def get_spotify_access_token(request):
    try:
        spotify = OAuth2Session(client_id, redirect_uri=redirect_uri)
        print(f"Code verifier in spotify_callback: {cache.get('code_verifier')}")

        # use fetch_token from OUath2Session to exchange auth code for access token
        token = spotify.fetch_token(
            'https://accounts.spotify.com/api/token',
            authorization_response=request.build_absolute_uri(),
            code=request.GET.get('code'),
            code_verifier=cache.get('code_verifier'),
            client_secret=client_secret
        )

        # store access token in session for later use
        utils.set_access_token(token['access_token'])
    except RequestException as e:
        print(f"A network error occured: {e}")
    except Exception as e:
        print(f"An error occurred during the get_spotify_access_token process: {e}")
        return HttpResponse(status=500)


def get_user_profile(request):
    """
    Get the user's profile information.
    """
    # access_token = cache.get('spotify_access_token')
    access_token = utils.get_access_token()

    if not access_token:
        return JsonResponse({"error": "Access token not found. Please authenticate with Spotify."}, status=401)
    
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    print(f"[{datetime.now()}] GET : Requesting User Profile")
    response = requests.get('https://api.spotify.com/v1/me', headers=headers)

    if response.status_code == 200:
        return JsonResponse(response.json(), safe=False)
    else:
        print("ERROR : Fetching user profile : ", response.text)
        return JsonResponse({"error": "Fetching user profile : " + response.text}, status=response.status_code)
    

def get_user_top_items(request, type, limit):
    """
    Get the user's top 20 tracks or artists.
    """
    # TODO: im currently saying its top 20, but it is actualy limit of results per request
    access_token = utils.get_access_token()

    if not access_token:
        return JsonResponse({"error": "Access token not found. Please authenticate with Spotify."}, status=401)
    
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    print(f"[{datetime.now()}] GET : Requesting User Top 20 {type}")
    response = requests.get(f'https://api.spotify.com/v1/me/top/{type}?limit={limit}', headers=headers)

    if response.status_code == 200:
        # return JsonResponse(response.json(), safe=False)
        return json.loads(response.text)
    else:
        print(f"ERROR : Fetching user top 20 {type} : ", response.text)
        return JsonResponse({"error": f"Fetching user top 20 {type} : " + response.text}, status=response.status_code)


def get_artist_genres(artist_id):
    """
    Get the genres of a given artist.
    """
    Artist = apps.get_model('backend', 'Artist')

    # Check if the artist exists in the database
    try:
        artist = Artist.objects.get(spotify_id=artist_id)
        if artist.genres:
            # If the artist has genres, return them
            return artist.genres
    except ObjectDoesNotExist:
        # If the artist doesn't exist in the database, continue to fetch genres from Spotify API
        pass

    access_token = utils.get_access_token()

    if not access_token:
        return JsonResponse({"error": "Access token not found. Please authenticate with Spotify."}, status=401)
    
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    print(f"[{datetime.now()}] GET : Requesting Artist Genres")
    response = requests.get(f'https://api.spotify.com/v1/artists/{artist_id}', headers=headers)
    response_json = response.json()
    genres = response_json['genres']

    print(f"GENRES : {genres}")
    if genres == []:
        response_json['genres'] = "No genres found for this artist"
        return genres

    if response.status_code == 200:
        return genres
    else:
        print("ERROR : Fetching artist genres : ", response.text)
        return JsonResponse({"error": "Fetching artist genres : " + response.text}, status=response.status_code)

# TODO: make code_verifier not global, per user
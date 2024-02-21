# import sys
# print(sys.path)
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.spotevent.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

import base64
import hashlib
# import os
import requests
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from requests_oauthlib import OAuth2Session

client_id = settings.SPOTIFY_CLIENT_ID
client_secret = settings.SPOTIFY_CLIENT_SECRET
redirect_uri = settings.SPOTIFY_REDIRECT_URI


def start_auth(request):
    """
    Start authentication process and redirect user to Spotify's authorization page.
    """
    spotify = OAuth2Session(client_id, redirect_uri=redirect_uri)

    # generate a code verifier
    # 40 bytes of random data, decoded to a utf-8 string
    code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode('utf-8')
    code_verifier = code_verifier[:128] # must be between 43 and 128 characters long


    # generate a code challenge
    # hash verifier with sha256 and url-safe base64 encode the result
    # decoded to a utf-8 string
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode('utf-8')).digest()).decode('utf-8').rstrip('=')

    # redirect user to Spotify authorization apge
    authorization_url, state = spotify.authorization_url(
        'https://accounts.spotify.com/authorize',
        code_challenge_method='S256',
        code_challenge=code_challenge
    )

    # store the state and code_verifier in the session for later to protect against CSRF
    request.session['oauth_state'] = state
    request.session['code_verifier'] = code_verifier

    return redirect(authorization_url)


def spotify_callback(request):
    """
    Callback for Spotify's authorization page.
    """
    spotify = OAuth2Session(client_id, redirect_uri=redirect_uri)

    # use fetch_token from OUath2Session to exchange auth code for access token
    token = spotify.fetch_token(
        'https://accounts.spotify.com/api/token',
        authorization_response=request.build_absolute_uri(),
        code=request.GET.get('code'),
        code_verifier=request.session['code_verifier'],
        client_secret=client_secret
    )

    # store access token in session for later use
    request.session['access_token'] = token['access_token']

    return redirect('http://localhost:3000')


def get_user_profile(request):
    """
    Get the user's profile information.
    """
    access_token = request.session['access_token']

    if not access_token:
        return "Access token not found. Please authenticate with Spotify."
    
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get('https://api.spotify.com/v1/me', headers=headers)

    if response.status_code == 200:
        print(response.json())
        return response.json()
    else:
        return "Error: " + response.text

# TODO: make code_verifier not global, per user
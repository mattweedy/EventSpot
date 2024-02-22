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
import string
import secrets
import requests
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from requests_oauthlib import OAuth2Session
from requests.exceptions import RequestException

client_id = settings.SPOTIFY_CLIENT_ID
client_secret = settings.SPOTIFY_CLIENT_SECRET
redirect_uri = settings.SPOTIFY_REDIRECT_URI
scope = 'user-read-private user-read-email'
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
        spotify = OAuth2Session(client_id, redirect_uri=redirect_uri)

        # generate a code verifier
        code_verifier = generate_code_verifier()

        # generate a code challenge
        # hash verifier with sha256 and url-safe base64 encode the result
        # decoded to a utf-8 string
        code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode('utf-8')).digest()).decode('utf-8').rstrip('=')

        # redirect user to Spotify authorization apge
        authorization_url, state = spotify.authorization_url(
            'https://accounts.spotify.com/authorize',
            # response_type='code',
            # scope=scope,
            code_challenge_method='S256',
            code_challenge=code_challenge,
        )

        # store the state and code_verifier in the session for later to protect against CSRF
        request.session['oauth_state'] = state
        request.session['code_verifier'] = code_verifier
        print(f"Code verifier in start_auth: {code_verifier}")

        return redirect(authorization_url)
    except Exception as e:
        print(f"An error occurred during the start_auth process: {e}")
        return HttpResponse(status=500)

def spotify_callback(request):
    """
    Callback for Spotify's authorization page.
    """
    try:
        spotify = OAuth2Session(client_id, redirect_uri=redirect_uri)
        print(f"Code verifier in spotify_callback: {request.session['code_verifier']}")

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
    except RequestException as e:
        print(f"An error occurred during the spotify_callback process: {e}")
        return HttpResponse(status=500)
    except KeyError:
        print("Code verifier not found in session.")
        return HttpResponse(status=500)


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
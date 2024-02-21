import sys
print(sys.path)
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

# generate a code verifier
# 40 bytes of random data, decoded to a utf-8 string
code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode('utf-8')
code_verifier = code_verifier[:128] # must be between 43 and 128 characters long

# generate a code challenge
# hash verifier with sha256 and url-safe base64 encode the result
# decoded to a utf-8 string
code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode('utf-8')).digest()).decode('utf-8')
code_challenge = code_challenge.replace('=', '') # remove any padding

# redirect user to Spotify authorization apge
authorization_url = f'https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&code_challenge_method=S256&code_challenge={code_challenge}'

# after user authorizes the app, Spotify will redirect to the redirect_uri with a code
# use code to get an access token

def start_auth(request):
    """
    Redirect user to Spotify's authorization page.
    """
    spotify = OAuth2Session(client_id, redirect_uri=redirect_uri)
    authorization_url, state = spotify.authorization_url('https://accounts.spotify.com/authorize')

    # store this state in the session for later to protect against CSRF
    request.session['oauth_state'] = state

    return redirect(authorization_url)


def spotify_callback(request):
    code = request.GET.get('code')
    if code is None:
        return HttpResponse('Error: no code provided', status=400)
    
    try:
        access_token = exchange_code_for_token(code)
    except Exception as e:
        return HttpResponse(f'Error: {str(e)}', status=500)
    
    return HttpResponse('Success', status=200)


def exchange_code_for_token(code):
    """
    Exchange a code for an access token.
    """
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'code_verifier': code_verifier,
    }

    response = requests.post('https://accounts.spotify.com/api/token', data=data)
    response.raise_for_status()

    access_token = response.json()['access_token']
    return access_token

# TODO: make code_verifier not global, per user
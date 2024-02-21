import base64
import hashlib
import os
import requests
from decouple import config
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

SPOTIFY_CLIENT_ID = config('SPOTIFY_CLIENT_ID')
SPOTIFY_REDIRECT_URI = config('SPOTIFY_REDIRECT_URI')

# client_id = 
redirect_uri = 'http://localhost:8000'

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

# POST request to Spotify's token endpoint
# note: the code_verifier is sent to the token endpoint
response = requests.post(
    'https://accounts.spotify.com/api/token',
    data={
        'client_id': client_id,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'code_verifier': code_verifier,
    },
)
access_token = response.json()['access_token']
import utils
from django.http import JsonResponse
from django.core.cache import cache
from datetime import datetime, timedelta
from django.shortcuts import redirect
from django.contrib.auth import logout
from .spotify_auth import get_user_profile, get_user_top_items


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
        return top_tracks
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
        # return JsonResponse(top_artists, safe=False)
        return top_artists
    except Exception as e:
        return JsonResponse({"error": str(e)})
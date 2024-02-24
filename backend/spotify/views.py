import utils
from django.http import JsonResponse
from django.core.cache import cache
from datetime import datetime, timedelta
from django.shortcuts import redirect
from django.contrib.auth import logout

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
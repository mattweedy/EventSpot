from django.http import JsonResponse
from django.core.cache import cache

def check_logged_in(request):
    """
    Check if the user is logged in.
    """
    try:
        access_token = cache.get('access_token')
        if access_token:
            print("User is logged in.")
            return JsonResponse({"logged_in": True})
        else:
            print("User is not logged in.")
            return JsonResponse({"logged_in": False})
    except Exception as e:
        print(f"An error occurred during the check_logged_in process: {e}")
        return JsonResponse({"logged_in": False})
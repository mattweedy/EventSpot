from django.core.cache import cache

def set_access_token(token):
    """
    Set the access token in the cache.
    """
    try:
        cache.set('spotify_access_token', token, 3600)
    except Exception as e:
        print(f"An error occurred during the set_access_token process: {e}")

def get_access_token():
    """
    Get the access token from the cache.
    """
    try:
        token = cache.get('spotify_access_token')
        return token
    except Exception as e:
        print(f"An error occurred during the get_access_token process: {e}")
        return None
    
def set_refresh_token(token):
    """
    Set the refresh token in the cache.
    """
    try:
        cache.set('spotify_refresh_token', token, 3600)  # Increased expiration time
        print("refresh token: ", cache.get('spotify_refresh_token'))
    except Exception as e:
        print(f"An error occurred during the set_refresh_token process: {e}")
        raise e  # Raise the exception after printing the error message

def get_refresh_token():
    """
    Get the refresh token from the cache.
    """
    try:
        print("refresh token 1 : ", cache.get('spotify_refresh_token'))
        token = cache.get('spotify_refresh_token')
        print("refresh token 2 : ", cache.get('spotify_refresh_token'))
        if token is None:
            print("No refresh token found.")
            # return None
        return token
    except Exception as e:
        print(f"An error occurred during the get_refresh_token process: {e}")
        raise e  # Raise the exception after printing the error message
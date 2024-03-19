import json
from . models import *
from . serializer import *
from . models import Venue, User
from rest_framework import viewsets
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . rec import main as get_recommendations_from_rec

class EventView(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class VenueView(viewsets.ModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer

class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@csrf_exempt
def apply_user_preferences(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = User.objects.get(username=data['username'])

        # update the user's preferences
        user.venue_preferences = data['venuePreferences']
        user.genre_preferences = data['genrePreferences']
        user.price_range = data['priceRange']
        user.queer_events = data['queerPreference']
        user.how_soon = data['howSoon']
        user.city = data['city']
        try:
            user.save()
        except Exception as e:
            return JsonResponse({'status': 'error', 'error': str(e)})

        return JsonResponse({'status': 'success : User preferences updated'})
    else:
        return JsonResponse({'status': 'error', 'error': 'Invalid request method'})
    
def get_user_preferences(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        user = User.objects.get(username=username)
        user_data = {
            'venue_preferences': user.venue_preferences,
            'genre_preferences': user.genre_preferences,
            'price_range': user.price_range,
            'queer_events': user.queer_events,
            'how_soon': user.how_soon,
            'city': user.city
        }
        return JsonResponse({'status': 'success', 'data': user_data})
    else:
        return JsonResponse({'status': 'error', 'error': 'Invalid request method'})


def get_recommendations(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        user = User.objects.get(username=username)
        user_data = UserSerializer(user).data

        # call the main function from rec.py to get the recommended event ids
        recommended_event_ids = get_recommendations_from_rec(username)
        print("returning...")

        return JsonResponse({'status': 'success', 'data': user_data, 'recommendations': recommended_event_ids})
    else:
        return JsonResponse({'status': 'error', 'error': 'Invalid request method'})
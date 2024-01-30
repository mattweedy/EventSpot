from django.http import JsonResponse
from .models import Event
from django.shortcuts import render

def get_events(request):
    events = Event.objects.all().values() # retrieve all events from db
    return JsonResponse({"events": list(events)})

def render_react(request):
    return render(request, "index.html")
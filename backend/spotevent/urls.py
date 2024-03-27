"""
URL configuration for SpotEvent project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib import admin
from backend.core.views import EventView, VenueView, UserView, apply_user_preferences, get_user_preferences, get_recommendations, save_remove_recommendation
from backend.spotify.spotify_auth import *
from backend.spotify.views import TrackView, ArtistView
from backend.spotify.views import check_logged_in, logout_view, user_profile, top_tracks, top_artists

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/events/', EventView.as_view({'get':'list'}), name='events'),
    path('api/venues/', VenueView.as_view({'get':'list'}), name='venues'),
    path('api/users/', UserView.as_view({'get':'list'}), name='users'),
    path('api/tracks/', TrackView.as_view({'get':'list'}), name='tracks'),
    path('api/artists/', ArtistView.as_view({'get':'list'}), name='artists'),
    path('api/set_preferences', apply_user_preferences, name='apply_user_preferences'),
    path('api/get_preferences', get_user_preferences, name='get_user_preferences'),
    path('api/recommendations', get_recommendations, name='get_recommendations'),
    path('api/save_remove_recommendation', save_remove_recommendation, name='save_remove_recommendation'),
    path('spotify/login', start_auth, name='start_auth'),
    path('spotify/logout', logout_view, name='logout'),
    path('spotify/callback', spotify_callback, name='spotify_callback'),
    path('spotify/profile', user_profile, name='get_user_profile'),
    path('spotify/logged_in', check_logged_in, name='check_logged_in'),
    path('spotify/top/tracks', top_tracks, name='get_user_top_items'),
    path('spotify/top/artists', top_artists, name='get_user_top_items'),
]

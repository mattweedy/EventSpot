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
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import EventView, VenueView
from core.spotify_auth import start_auth

router = DefaultRouter()
router.register(r'events', EventView, basename='events')
router.register(r'venues', VenueView, basename='venues')

# urlpatterns = [
#     path("admin/", admin.site.urls),
#     path("", include(router.urls)),
# ]

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/events/', EventView.as_view({'get':'list'}), name='events'),
    path('api/venues/', VenueView.as_view({'get':'list'}), name='venues'),
    path('api/spotify/login', start_auth, name='start_auth'),
]

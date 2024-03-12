from rest_framework import serializers
from . models import Track, Artist

class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = '__all__'

class ArtistSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Artist
        fields = '__all__'
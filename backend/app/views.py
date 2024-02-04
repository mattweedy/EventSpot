from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializer import *

class ReactView(APIView):
    def get(self, request):
        output = [{"event_name": output.event_name,
                   "event_genre": output.event_genre}
                   for output in Event.objects.all()]
        return Response(output)
    def post(self, request):
        serializer = ReactSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
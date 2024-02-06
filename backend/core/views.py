from django.shortcuts import render
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from . models import *
from . serializer import *

# class EventView(APIView):
#     def get(self, request):
#         output = [{"name": output.name,
#                    "venue_id": output.venue_id}
#                    for output in Event.objects.all()]
#         return Response(output)
#     def post(self, request):
#         serializer = EventSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
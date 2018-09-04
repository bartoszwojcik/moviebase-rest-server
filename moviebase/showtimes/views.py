from rest_framework import generics
from showtimes.models import Cinema
from showtimes.serializers import CinemaSerializer
from django.views.generic import detail


class CinemaListView(generics.ListCreateAPIView):
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer


class CinemaView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer


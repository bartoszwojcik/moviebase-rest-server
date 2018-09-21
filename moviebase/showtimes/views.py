from rest_framework import generics
from showtimes.models import Cinema, Screening
from showtimes.serializers import CinemaSerializer, ScreeningSerializer


class CinemaListView(generics.ListCreateAPIView):
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer


class CinemaView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer


class ScreeningsListView(generics.ListCreateAPIView):
    queryset = Screening.objects.all()
    serializer_class = ScreeningSerializer
    search_fields = ('movie__title', 'cinema__city')


class ScreeningView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Screening.objects.all()
    serializer_class = ScreeningSerializer

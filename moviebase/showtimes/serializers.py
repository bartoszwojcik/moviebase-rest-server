from rest_framework import serializers
from movielist.models import Movie
from showtimes.models import Cinema


class CinemaSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Cinema
        fields = "__all__"

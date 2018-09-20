from rest_framework import serializers
from movielist.models import Movie
from showtimes.models import Cinema, Screening


class CinemaSerializer(serializers.HyperlinkedModelSerializer):
    # movies = serializers.SlugRelatedField(
    #     slug_field='title',
    #     queryset=Movie.objects.all(),
    #     many=True
    # )

    class Meta:
        model = Cinema
        fields = ["url", "name", "city", "movies"]
        # fields = "__all__"


class ScreeningSerializer(serializers.HyperlinkedModelSerializer):
    cinema = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Cinema.objects.all()
    )
    movie = serializers.SlugRelatedField(
        slug_field="title",
        queryset=Movie.objects.all()
    )

    class Meta:
        model = Screening
        fields = "__all__"

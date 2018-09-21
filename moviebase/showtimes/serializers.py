from rest_framework import serializers
from movielist.models import Movie
from showtimes.models import Cinema, Screening
import datetime

today = datetime.date.today()


class CinemaSerializer(serializers.HyperlinkedModelSerializer):

    movies = serializers.SerializerMethodField()

    def get_movies(self, cinema):
        screening_data = Screening.objects.filter(
            date__date__range=(today, today + datetime.timedelta(days=30))
        )
        serializer = LimitedScreeningSerializer(
            instance=screening_data,
            many=True,
            context=self.context
        )
        return serializer.data

    class Meta:
        model = Cinema
        fields = ["url", "name", "city", "movies"]


class LimitedScreeningSerializer(serializers.ModelSerializer):
    movie = serializers.SlugRelatedField(
        slug_field='title', queryset=Movie.objects.all()
    )

    class Meta:
        model = Screening
        fields = ["movie", "date"]


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

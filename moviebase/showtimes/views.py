from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse as rest_reverse

from moviebase.serializers import UserSerializer, UserSerializerWithToken
from showtimes.models import Cinema, Screening
from showtimes.serializers import CinemaSerializer, ScreeningSerializer

# General views

@api_view(["GET"])
def api_root(request, format=None):
    return Response({
        "Cinemas": rest_reverse("cinemas", request=request, format=format),
        "Movies": rest_reverse("movies", request=request, format=format),
        "Screenings": rest_reverse(
            "screenings", request=request, format=format
        ),
    })


# User-related views

@api_view(['GET'])
def current_user(request):
    """
    Determine the current user using the token, and return user data. If token
    is found in the browser, the client should make a request to this view.
    :return: serialized response with data of a user associated with the token
    """

    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class UserListView(generics.ListAPIView):
    """
    API endpoint for listing available users.
    """

    permission_classes = (permissions.AllowAny,)

    queryset = User.objects.all()
    serializer_class = UserSerializer


    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(generics.RetrieveAPIView):
    """
    API endpoint with single user details.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer


# Cinema views

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

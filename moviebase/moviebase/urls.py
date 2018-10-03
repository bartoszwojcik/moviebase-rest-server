"""moviebase URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, re_path
from django.contrib import admin
from django.urls import include

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.schemas import get_schema_view
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, \
    verify_jwt_token

from movielist.views import MovieListView, MovieView
from showtimes.views import CinemaListView, CinemaView, ScreeningsListView, \
    ScreeningView, api_root, UserListView, UserDetailView, current_user

schema_view = get_schema_view(title="MovieBase API")

urlpatterns = [
    # Main views
    re_path(r'^admin/', admin.site.urls),
    re_path(r"^$", api_root),
    re_path(r"schema/?$", schema_view),

    # User views
    re_path(
        r'^users/?$',
        UserListView.as_view(),
        name="users"
    ),
    re_path(
        r'^users/(?P<pk>[0-9]+)/?$',
        UserDetailView.as_view(),
        name="user-detail"
    ),
    re_path(r"^current_user/?$", current_user),

    # Movies
    re_path(r'^movies/?$', MovieListView.as_view(), name="movies"),
    re_path(
        r'^movies/(?P<pk>[0-9]+)/?$', MovieView.as_view(), name="movie-detail"
    ),

    # Cinemas
    re_path(
        r'^cinemas/?$', CinemaListView.as_view(), name="cinemas"
    ),
    re_path(
        r'^cinemas/(?P<pk>[0-9]+)/?$',
        CinemaView.as_view(),
        name="cinema-detail"
    ),

    # Screenings
    re_path(
        r'^screenings/?$', ScreeningsListView.as_view(), name="screenings"
    ),
    re_path(
        r'^screenings/(?P<pk>[0-9]+)/?$',
        ScreeningView.as_view(),
        name="screening-detail"
    ),
]


# Allow .json etc. file formats directly in URLs
urlpatterns = format_suffix_patterns(urlpatterns)

# For providing login to browsable API
urlpatterns += [
    re_path(r'^api-auth/', include('rest_framework.urls')),
]

# # JWT Token
urlpatterns += [
    re_path(r'^api-token-auth/', obtain_jwt_token),
    re_path(r'^api-token-refresh/', refresh_jwt_token),
    re_path(r'^api-token-verify/', verify_jwt_token),
]

from django.urls import include, path

from . import api


urlpatterns = [
  path("songs/", api.SongListAPI.as_view(), name="songs"),
  path("songs/<int:pk>", api.SongDetailAPI.as_view(), name="songs"),
]
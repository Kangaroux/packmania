from django.urls import include, path

from . import api


urlpatterns = [
  path("session/", api.SessionAPI.as_view(), name="session"),
  path("users/", api.UserListAPI.as_view(), name="users"),
  path("users/<int:pk>", api.UserDetailAPI.as_view(), name="users"),
]
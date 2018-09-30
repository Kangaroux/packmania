from django.urls import include, path
from rest_framework import routers

from . import api


urlpatterns = [
  path("session/", api.SessionAPI.as_view(), name="session"),
  path("users/", api.UserList.as_view(), name="users"),
  path("users/<int:pk>", api.UserDetail.as_view(), name="users"),
]
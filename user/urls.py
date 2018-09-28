from django.urls import include, path
from rest_framework import routers

from . import views


urlpatterns = [
  path("users", views.UserList.as_view(), name="users"),
  path("users/<int:pk>", views.UserDetail.as_view(), name="users"),
]
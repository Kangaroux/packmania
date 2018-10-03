from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
  username = models.CharField("username", max_length=20, unique=True,
    error_messages={
      "unique": "A user with that username already exists."
    })

  email = models.EmailField("email", unique=True,
    error_messages={
      "unique": "A user with that email already exists."
    })

  # Users are required to login using their email
  USERNAME_FIELD = "email"
  REQUIRED_FIELDS = [ "username" ]
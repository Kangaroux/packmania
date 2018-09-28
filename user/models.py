from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
  username = models.SlugField(max_length=20, unique=True,
    error_messages={
      "invalid": "Can only contain letters, numbers, hyphens, and underscores.",
      "unique": "A user with that username already exists.",
    })

  email = models.EmailField(unique=True,
    error_messages={
      "unique": "A user with that email already exists.",
    })
import re

from rest_framework import serializers
from rest_framework.serializers import ValidationError

from config.messages import error_messages
from .models import User


class CreateUserSerializer(serializers.ModelSerializer):
  """ Used for POST/PATCH """

  class Meta:
    model = User
    fields = ("email", "username", "password")
    extra_kwargs = {
      "email": { **error_messages() },
      "username": { "min_length": 2, **error_messages({
          "invalid": "Can only contain letters, numbers, hyphens, and underscores."
        })
      },
      "password": { "min_length": 8, **error_messages() }
    }

  def validate_username(self, val):
    if not re.search(r"[a-zA-Z\d]", val):
      raise ValidationError("Must contain at least one letter or number.")

    return val


class DetailUserSerializer(serializers.ModelSerializer):
  """ Used for GET """

  class Meta:
    model = User
    fields = ("id", "email", "username", "date_joined")

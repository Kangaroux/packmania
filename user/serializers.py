import re

from rest_framework import serializers
from rest_framework.fields import CharField
from rest_framework.serializers import ValidationError

from lib.errors import error_messages
from .models import User


# Fields on the user model which are only visible to the user who owns them and admins
PRIVATE_FIELDS = ("email",)


class UserSerializer(serializers.ModelSerializer):

  # We won't require users to give their current password in order to change it
  confirm_password = CharField(max_length=100, trim_whitespace=False, write_only=True)

  class Meta:
    model = User
    fields = ("id", "date_joined", "email", "username", "password", "confirm_password")
    extra_kwargs = {
      "id": {
        "read_only": True,
      },

      "email": {
        **error_messages()
      },

      "username": {
        **error_messages(),
        "min_length": 2
      },

      "confirm_password": {
        **error_messages(),
        "min_length": 8
      },

      "password": {
        **error_messages(),
        "min_length": 8,
        "write_only": True
      }
    }

  def __init__(self, *args, **kwargs):
    self.show_private_fields = kwargs.pop("show_private_fields", False)
    super().__init__(*args, **kwargs)

  def validate_username(self, val):
    if not re.fullmatch(r"[a-zA-Z\d\-_]+", val):
      raise ValidationError("Can only contain letters, numbers, hyphens, and underscores.")
    elif not re.search(r"[a-zA-Z\d]", val):
      raise ValidationError("Must contain at least one letter or number.")

    return val

  def validate(self, data):
    password = data.get("password")
    confirm = data.get("confirm_password")

    if (password or confirm) and password != confirm:
      raise ValidationError({
        "confirm_password": "Passwords must match.",
        "password": "Passwords must match.",
      })

    return data

  def create(self, data):
    data_copy = { **data }
    data_copy.pop("confirm_password", None)

    user = User(**data_copy)
    user.set_password(data_copy.get("password"))
    user.save()

    return user

  def update(self, instance, data):
    instance.email = data.get("email", instance.email)
    instance.username = data.get("username", instance.username)

    if "password" in data:
      instance.set_password(data.get("password"))

    instance.save()

    return instance

  @property
  def data(self):
    data = super().data

    if not self.show_private_fields:
      for field in PRIVATE_FIELDS:
        data.pop(field, None)

    return data
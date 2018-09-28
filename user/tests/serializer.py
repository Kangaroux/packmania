import re

from django.shortcuts import reverse
from django.test import Client, TestCase

from ..models import User
from ..serializers import UserSerializer


class TestSerializer(TestCase):
  def test_serialize_user_instance(self):
    u = User.objects.create(
      username="test_user",
      email="test@test.com"
    )

    # For UTC, Python formats dates with a "+00:00" suffix, whereas DRF uses "Z"
    self.assertEqual(UserSerializer(u).data, {
      "id": u.id,
      "username": "test_user",
      "email": "test@test.com",
      "date_joined": re.sub(r"\+.*", "Z", u.date_joined.isoformat())
    })
from django.shortcuts import reverse
from django.test import Client, TestCase

from user.models import User
from user.serializers import UserSerializer


class TestGetUsers(TestCase):
  def test_get_all(self):
    User.objects.all().delete()

    users = [
      User.objects.create(username="test-user-1", email="test1@test.com"),
      User.objects.create(username="test-user-2", email="test2@test.com"),
      User.objects.create(username="test-user-3", email="test3@test.com"),
    ]

    c = Client()
    resp = sorted(c.get(reverse("api:users")).json()["results"], key=lambda x: x["id"])

    self.assertEqual(resp, UserSerializer(users, many=True).data)
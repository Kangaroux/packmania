from django.shortcuts import reverse
from django.test import Client, TestCase

from ..models import User
from ..serializers import DetailUserSerializer


class TestGetUsers(TestCase):
  def setUp(self):
    User.objects.all().delete()

  def test_get_all(self):
    users = [
      User.objects.create(username="test-user-1", email="test1@test.com"),
      User.objects.create(username="test-user-2", email="test2@test.com"),
      User.objects.create(username="test-user-3", email="test3@test.com"),
    ]

    c = Client()
    resp = sorted(c.get(reverse("api:users")).json(), key=lambda x: x["id"])

    self.assertEqual(resp, DetailUserSerializer(users, many=True).data)
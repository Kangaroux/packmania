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

  def test_get_self(self):
    u = User.objects.create(username="test_user", email="test@test.com")
    c = Client()
    c.force_login(u)
    resp = c.get(reverse("api:users", kwargs={ "pk": u.id }))

    self.assertEqual(resp.status_code, 200)
    self.assertEqual(resp.json()["user"], UserSerializer(u, show_private_fields=True).data)

  def test_get_other_user_logged_in(self):
    u1 = User.objects.create(username="test_user", email="test@test.com")
    u2 = User.objects.create(username="another_user", email="another@user.com")
    c = Client()
    c.force_login(u1)
    resp = c.get(reverse("api:users", kwargs={ "pk": u2.id }))

    self.assertEqual(resp.status_code, 200)
    self.assertEqual(resp.json()["user"], UserSerializer(u2).data)

  def test_get_user_not_logged_in(self):
    u = User.objects.create(username="test_user", email="test@test.com")
    c = Client()
    resp = c.get(reverse("api:users", kwargs={ "pk": u.id }))

    self.assertEqual(resp.status_code, 200)
    self.assertEqual(resp.json()["user"], UserSerializer(u).data)
from django.shortcuts import reverse
from django.test import TestCase

from user.models import User
from user.serializers import UserSerializer


class TestGetUsers(TestCase):
  def test_get_all(self):
    users = [
      User.objects.create_user("test-user-1", "test1@test.com"),
      User.objects.create_user("test-user-2", "test2@test.com"),
      User.objects.create_user("test-user-3", "test3@test.com"),
    ]

    resp = sorted(self.client.get(reverse("api:users")).json()["results"], key=lambda x: x["id"])

    self.assertEqual(resp, UserSerializer(users, many=True).data)

  def test_get_self(self):
    u = User.objects.create_user("test_user", "test@test.com")
    self.client.force_login(u)
    resp = self.client.get(reverse("api:users", kwargs={ "pk": u.id }))

    self.assertEqual(resp.status_code, 200)
    self.assertEqual(resp.json()["user"], UserSerializer(u, show_private_fields=True).data)

  def test_get_other_user_logged_in(self):
    u1 = User.objects.create_user("test_user", "test@test.com")
    u2 = User.objects.create_user("another_user", "another@user.com")
    self.client.force_login(u1)
    resp = self.client.get(reverse("api:users", kwargs={ "pk": u2.id }))

    self.assertEqual(resp.status_code, 200)
    self.assertEqual(resp.json()["user"], UserSerializer(u2).data)

  def test_get_user_not_logged_in(self):
    u = User.objects.create_user("test_user", "test@test.com")
    resp = self.client.get(reverse("api:users", kwargs={ "pk": u.id }))

    self.assertEqual(resp.status_code, 200)
    self.assertEqual(resp.json()["user"], UserSerializer(u).data)
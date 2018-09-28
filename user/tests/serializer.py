import re

from django.shortcuts import reverse
from django.test import Client, TestCase

from ..models import User
from ..serializers import UserSerializer


class TestSerializer(TestCase):
  def setUp(self):
    User.objects.all().delete()

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

  def test_create_user(self):
    u = UserSerializer().create({
      "username": "test_user",
      "email": "test@test.com",
      "password": "testpass"
    })

    self.assertEqual(u, User.objects.get(username="test_user"))
    self.assertTrue(u.check_password("testpass"))

  def test_update_user(self):
    u = User(username="test_user", email="test@test.com")
    u.set_password("password123")
    u.save()

    user_id = u.id

    UserSerializer().update(u, {
      "username": "new",
      "email": "new@test.com",
      "password": "NewPassword"
    })

    self.assertEqual(u.id, user_id)
    self.assertEqual(u.username, "new")
    self.assertEqual(u.email, "new@test.com")
    self.assertTrue(u.check_password("NewPassword"))
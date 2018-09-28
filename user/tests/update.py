from django.shortcuts import reverse
from django.test import Client, TestCase

from ..models import User
from ..serializers import UserSerializer


class TestUpdateUsers(TestCase):
  def setUp(self):
    User.objects.all().delete()
    self.u = User(username="test_user", email="test@test.com")
    self.u.set_password("password123")
    self.u.save()

  def test_update_ok(self):
    c = Client()
    resp = c.patch(reverse("api:users", kwargs={ "pk": self.u.id }), {
      "username": "new_username",
      "email": "newemail@test.com",
      "password": "mynewpass",
      "confirm_password": "mynewpass"
    }, content_type="application/json")

    self.assertEqual(resp.status_code, 200)
    self.assertNotEqual(resp.json()["user"], UserSerializer(self.u).data)

    # Pull down the new user model
    self.u.refresh_from_db()

    self.assertEqual(resp.json()["user"], UserSerializer(self.u).data)
    self.assertTrue(self.u.check_password("mynewpass"))
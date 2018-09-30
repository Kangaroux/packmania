from django.contrib.auth.models import Permission
from django.shortcuts import reverse
from django.test import Client, TestCase

from user.models import User
from user.serializers import UserSerializer


class TestUpdateUsers(TestCase):
  def setUp(self):
    User.objects.all().delete()
    self.u = User(username="test_user", email="test@test.com")
    self.u.set_password("password123")
    self.u.save()

  def test_update_self_ok(self):
    c = Client()
    c.force_login(self.u)
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

  def test_update_not_logged_in(self):
    old_data = UserSerializer(self.u).data

    c = Client()
    resp = c.patch(reverse("api:users", kwargs={ "pk": self.u.id }), {
      "username": "new_username",
      "email": "newemail@test.com",
      "password": "mynewpass",
      "confirm_password": "mynewpass"
    }, content_type="application/json")

    self.u.refresh_from_db()

    self.assertEqual(resp.status_code, 401)
    self.assertEqual(resp.json()["msg"], "You must be logged in to do that.")
    self.assertEqual(UserSerializer(self.u).data, old_data)

  def test_update_lacks_permission(self):
    user2 = User.objects.create(username="another_user", email="another@user.com")
    old_data = UserSerializer(user2).data

    c = Client()
    c.force_login(self.u)
    resp = c.patch(reverse("api:users", kwargs={ "pk": user2.id }), {
      "username": "new_username",
      "email": "newemail@test.com",
      "password": "mynewpass",
      "confirm_password": "mynewpass"
    }, content_type="application/json")

    user2.refresh_from_db()

    self.assertEqual(resp.status_code, 403)
    self.assertEqual(resp.json()["msg"], "You do not have permission to do that.")
    self.assertEqual(old_data, UserSerializer(user2).data)
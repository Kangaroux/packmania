from django.contrib.auth.models import Permission
from django.shortcuts import reverse
from django.test import TestCase

from user.models import User
from user.serializers import UserSerializer


class TestUpdateUsers(TestCase):
  @classmethod
  def setUpTestData(cls):
    cls.u = User.objects.create_user("test_user", "test@test.com", "password123")
    cls.u2 = User.objects.create_user("test_user2", "test2@test.com", "password123")

  def setUp(self):
    self.u.refresh_from_db()
    self.u2.refresh_from_db()


  def test_update_self_ok(self):
    self.client.force_login(self.u)
    resp = self.client.patch(reverse("api:users", kwargs={ "pk": self.u.id }), {
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
    resp = self.client.patch(reverse("api:users", kwargs={ "pk": self.u.id }), {
      "username": "new_username",
      "email": "newemail@test.com",
      "password": "mynewpass",
      "confirm_password": "mynewpass"
    }, content_type="application/json")

    self.u.refresh_from_db()

    self.assertEqual(resp.status_code, 401)
    self.assertEqual(resp.json()["msg"], "You must be logged in to do that.")
    self.assertTrue(self.u.check_password("password123"))
    self.assertEqual(UserSerializer(self.u).data, old_data)

  def test_update_lacks_permission(self):
    self.client.force_login(self.u)

    old_data = UserSerializer(self.u2).data
    resp = self.client.patch(reverse("api:users", kwargs={ "pk": self.u2.id }), {
      "username": "new_username",
      "email": "newemail@test.com",
      "password": "mynewpass",
      "confirm_password": "mynewpass"
    }, content_type="application/json")

    self.u2.refresh_from_db()

    self.assertEqual(resp.status_code, 403)
    self.assertEqual(resp.json()["msg"], "You do not have permission to do that.")
    self.assertEqual(old_data, UserSerializer(self.u2).data)
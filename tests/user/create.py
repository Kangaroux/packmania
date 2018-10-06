from django.contrib import auth
from django.shortcuts import reverse
from django.test import TestCase

from user.models import User
from user.serializers import UserSerializer


class TestCreateUser(TestCase):
  def test_create_ok(self):
    resp = self.client.post(reverse("api:users"), {
      "username": "test_user",
      "email": "test@test.com",
      "password": "password123",
      "confirm_password": "password123"
    })

    user = User.objects.get(pk=resp.json()["user"]["id"])

    self.assertEqual(resp.status_code, 201)
    self.assertEqual(UserSerializer(user).data, resp.json()["user"])

  def test_missing_params(self):
    resp = self.client.post(reverse("api:users"), {})

    self.assertEqual(resp.status_code, 400)
    self.assertEqual(resp.json()["fields"], {
      "email": "This field is required.",
      "username": "This field is required.",
      "password": "This field is required.",
      "confirm_password": "This field is required.",
    })

  def test_logged_in_user(self):
    u = User.objects.create_user(username="blah", email="blah@blah.com")

    self.client.force_login(u)

    resp = self.client.post(reverse("api:users"), {
      "username": "test_user",
      "email": "test@test.com",
      "password": "password123",
      "confirm_password": "password123"
    })

    self.assertEqual(resp.status_code, 400)
    self.assertEqual(resp.json()["msg"], "Logout before trying to create a new user.")

    # Still logged in
    self.assertTrue(auth.get_user(self.client).is_authenticated)

  def test_bad_email(self):
    resp = self.client.post(reverse("api:users"), { "email": "bad@email" })

    self.assertEqual(resp.status_code, 400)
    self.assertEqual(resp.json()["fields"]["email"], "Enter a valid email address.")

  def test_email_already_taken(self):
    User.objects.create_user("test_user", "test@test.com")

    resp = self.client.post(reverse("api:users"), { "email": "test@test.com" })

    self.assertEqual(resp.status_code, 400)
    self.assertEqual(resp.json()["fields"]["email"], "Email is already in use.")

  def test_short_username(self):
    resp = self.client.post(reverse("api:users"), { "username": "a" })

    self.assertEqual(resp.status_code, 400)
    self.assertEqual(resp.json()["fields"]["username"], "Must be at least 2 characters.")

  def test_long_username(self):
    resp = self.client.post(reverse("api:users"), { "username": "a" * 50 })

    self.assertEqual(resp.status_code, 400)
    self.assertEqual(resp.json()["fields"]["username"], "Cannot be longer than 20 characters.")

  def test_bad_username_slug(self):
    resp = self.client.post(reverse("api:users"), { "username": "bad username!" })

    self.assertEqual(resp.status_code, 400)
    self.assertEqual(resp.json()["fields"]["username"],
      "Can only contain letters, numbers, hyphens, and underscores.")

  def test_bad_username_no_letter_or_number(self):
    resp = self.client.post(reverse("api:users"), { "username": "-_" })

    self.assertEqual(resp.status_code, 400)
    self.assertEqual(resp.json()["fields"]["username"],
      "Must contain at least one letter or number.")

  def test_username_already_taken(self):
    User.objects.create_user("test_user", "test@test.com")

    resp = self.client.post(reverse("api:users"), { "username": "test_user" })

    self.assertEqual(resp.status_code, 400)
    self.assertEqual(resp.json()["fields"]["username"], "Username is already taken.")

  def test_short_password(self):
    resp = self.client.post(reverse("api:users"), { "password": "12345" })

    self.assertEqual(resp.status_code, 400)
    self.assertEqual(resp.json()["fields"]["password"], "Must be at least 6 characters.")
from django.shortcuts import reverse
from django.test import Client, TestCase

from user.models import User
from user.serializers import UserSerializer


class TestCreateUser(TestCase):
  def test_create_ok(self):
    c = Client()
    resp = c.post(reverse("api:users"), {
      "username": "test_user",
      "email": "test@test.com",
      "password": "password123",
      "confirm_password": "password123"
    })

    self.assertTrue(resp.status_code, 200)
    user = User.objects.get(pk=resp.json()["user"]["id"])
    self.assertEqual(UserSerializer(user).data, resp.json()["user"])

  def test_missing_params(self):
    c = Client()
    resp = c.post(reverse("api:users"), {})

    self.assertEqual(resp.status_code, 400)
    self.assertEqual(resp.json()["fields"], {
      "email": "This field is required.",
      "username": "This field is required.",
      "password": "This field is required.",
      "confirm_password": "This field is required.",
    })

  def test_bad_email(self):
    c = Client()
    resp = c.post(reverse("api:users"), { "email": "bad@email" })

    self.assertEqual(resp.status_code, 400)
    self.assertEqual(resp.json()["fields"]["email"], "Enter a valid email address.")

  def test_email_already_taken(self):
    User.objects.create(email="test@test.com")

    c = Client()
    resp = c.post(reverse("api:users"), { "email": "test@test.com" })

    self.assertEqual(resp.status_code, 400)
    self.assertEqual(resp.json()["fields"]["email"], "A user with that email already exists.")

  def test_short_username(self):
    c = Client()
    resp = c.post(reverse("api:users"), { "username": "a" })

    self.assertEqual(resp.status_code, 400)
    self.assertEqual(resp.json()["fields"]["username"], "Must be at least 2 characters.")

  def test_long_username(self):
    c = Client()
    resp = c.post(reverse("api:users"), { "username": "a" * 50 })

    self.assertEqual(resp.status_code, 400)
    self.assertEqual(resp.json()["fields"]["username"], "Cannot be longer than 20 characters.")

  def test_bad_username_slug(self):
    c = Client()
    resp = c.post(reverse("api:users"), { "username": "bad username!" })

    self.assertEqual(resp.status_code, 400)
    self.assertEqual(resp.json()["fields"]["username"],
      "Can only contain letters, numbers, hyphens, and underscores.")

  def test_bad_username_no_letter_or_number(self):
    c = Client()
    resp = c.post(reverse("api:users"), { "username": "-_" })

    self.assertEqual(resp.status_code, 400)
    self.assertEqual(resp.json()["fields"]["username"],
      "Must contain at least one letter or number.")

  def test_short_password(self):
    c = Client()
    resp = c.post(reverse("api:users"), { "password": "1234567" })

    self.assertEqual(resp.status_code, 400)
    self.assertEqual(resp.json()["fields"]["password"], "Must be at least 8 characters.")
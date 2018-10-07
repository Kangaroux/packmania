from django.shortcuts import reverse
from django.test import TestCase

from user.models import User
from user.serializers import UserSerializer


class TestSessionAPI(TestCase):
  @classmethod
  def setUpTestData(cls):
    cls.password = "password"
    cls.u = User.objects.create_user("test_user", "test@test.com", cls.password)


  def test_not_logged_in(self):
    resp = self.client.get(reverse("api:session"))

    self.assertEqual(resp.json()["authenticated"], False)
    self.assertEqual(resp.json()["user"], None)

  def test_logged_in(self):
    self.client.force_login(self.u)
    resp = self.client.get(reverse("api:session"))

    self.assertEqual(resp.json()["authenticated"], True)
    self.assertEqual(resp.json()["user"], UserSerializer(self.u, show_private_fields=True).data)

  def test_login_ok(self):
    resp = self.client.post(reverse("api:session"), {
      "email": self.u.email,
      "password": self.password
    })

    self.assertEqual(resp.status_code, 200)
    self.assertEqual(resp.json()["user"], UserSerializer(self.u, show_private_fields=True).data)
    self.assertTrue(self.client.session.get_expire_at_browser_close())

  def test_login_remember_me(self):
    resp = self.client.post(reverse("api:session"), {
      "email": self.u.email,
      "password": self.password,
      "remember_me": None
    })

    self.assertEqual(resp.status_code, 200)
    self.assertEqual(resp.json()["user"], UserSerializer(self.u, show_private_fields=True).data)
    self.assertFalse(self.client.session.get_expire_at_browser_close())

  def test_login_missing_credentials(self):
    resp = self.client.post(reverse("api:session"))

    self.assertEqual(resp.status_code, 400)
    self.assertEqual(resp.json()["fields"], {
      "email": "This field is required.",
      "password": "This field is required.",
    })

  def test_login_ok_case_insensitive_email(self):
    resp = self.client.post(reverse("api:session"), {
      "email": self.u.email.upper(),
      "password": self.password
    })

    self.assertEqual(resp.status_code, 200)
    self.assertEqual(resp.json()["user"], UserSerializer(self.u, show_private_fields=True).data)

  def test_login_bad_email(self):
    resp = self.client.post(reverse("api:session"), {
      "email": "wrong@email.com",
      "password": self.password
    })

    self.assertEqual(resp.status_code, 400)
    self.assertEqual(resp.json()["fields"], {
      "email": "Email or password is incorrect.",
      "password": "Email or password is incorrect.",
    })

  def test_login_bad_password(self):
    resp = self.client.post(reverse("api:session"), {
      "email": self.u.email,
      "password": "badpassword"
    })

    self.assertEqual(resp.status_code, 400)
    self.assertEqual(resp.json()["fields"], {
      "email": "Email or password is incorrect.",
      "password": "Email or password is incorrect.",
    })

  def test_logout(self):
    self.client.force_login(self.u)
    resp = self.client.delete(reverse("api:session"))

    self.assertEqual(resp.status_code, 200)
    self.assertEqual(self.client.session.get("_auth_user_id"), None)
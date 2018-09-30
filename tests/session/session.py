from django.shortcuts import reverse
from django.test import Client, TestCase

from user.models import User


class TestSessionAPI(TestCase):
  def setUp(self):
    self.password = "password"
    self.u = User(username="test_user", email="test@test.com")
    self.u.set_password(self.password)
    self.u.save()

  def test_not_logged_in(self):
    c = Client()
    resp = c.get(reverse("api:session"))

    self.assertEqual(resp.json()["authenticated"], False)
    self.assertEqual(resp.json()["user_id"], None)

  def test_logged_in(self):
    c = Client()
    c.force_login(self.u)
    resp = c.get(reverse("api:session"))

    self.assertEqual(resp.json()["authenticated"], True)
    self.assertEqual(resp.json()["user_id"], self.u.id)

  def test_login_ok(self):
    c = Client()
    resp = c.post(reverse("api:session"), {
      "email": self.u.email,
      "password": self.password
    })

    self.assertEqual(resp.status_code, 200)
    self.assertEqual(resp.json()["user_id"], self.u.id)

  def test_login_missing_credentials(self):
    c = Client()
    resp = c.post(reverse("api:session"))

    self.assertEqual(resp.status_code, 400)
    self.assertEqual(resp.json()["fields"], {
      "email": "This field is required.",
      "password": "This field is required.",
    })

  def test_login_ok_case_insensitive_email(self):
    c = Client()
    resp = c.post(reverse("api:session"), {
      "email": self.u.email.upper(),
      "password": self.password
    })

    self.assertEqual(resp.status_code, 200)
    self.assertEqual(resp.json()["user_id"], self.u.id)

  def test_login_bad_email(self):
    c = Client()
    resp = c.post(reverse("api:session"), {
      "email": "wrong@email.com",
      "password": self.password
    })

    self.assertEqual(resp.status_code, 400)
    self.assertEqual(resp.json()["fields"], {
      "email": "Email or password is incorrect.",
      "password": "Email or password is incorrect.",
    })

  def test_login_bad_password(self):
    c = Client()
    resp = c.post(reverse("api:session"), {
      "email": self.u.email,
      "password": "badpassword"
    })

    self.assertEqual(resp.status_code, 400)
    self.assertEqual(resp.json()["fields"], {
      "email": "Email or password is incorrect.",
      "password": "Email or password is incorrect.",
    })

  def test_logout(self):
    c = Client()
    c.force_login(self.u)
    resp = c.delete(reverse("api:session"))

    self.assertEqual(resp.status_code, 200)
    self.assertEqual(c.session.get("_auth_user_id"), None)
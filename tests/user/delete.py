from django.contrib.auth.models import Permission
from django.shortcuts import reverse
from django.test import Client, TestCase

from user.models import User
from user.serializers import UserSerializer


class TestDeleteUser(TestCase):
  def setUp(self):
    User.objects.all().delete()

  def test_delete_self_ok(self):
    u = User.objects.create(username="test_user", email="test@test.com")
    c = Client()
    c.force_login(u)
    resp = c.delete(reverse("api:users", kwargs={ "pk": u.id }))

    u.refresh_from_db()

    self.assertEqual(resp.status_code, 200)
    self.assertEqual(u.is_active, False)

  def test_delete_not_logged_in(self):
    u = User.objects.create(username="test_user", email="test@test.com")
    c = Client()
    resp = c.delete(reverse("api:users", kwargs={ "pk": u.id }))

    u.refresh_from_db()

    self.assertEqual(resp.status_code, 401)
    self.assertEqual(resp.json()["msg"], "You must be logged in to do that.")
    self.assertEqual(u.is_active, True)

  def test_delete_lacks_permission(self):
    u1 = User.objects.create(username="test_user", email="test@test.com")
    u2 = User.objects.create(username="another_user", email="another@user.com")

    c = Client()
    c.force_login(u1)
    resp = c.delete(reverse("api:users", kwargs={ "pk": u2.id }))

    u2.refresh_from_db()

    self.assertEqual(resp.status_code, 403)
    self.assertEqual(resp.json()["msg"], "You do not have permission to do that.")
    self.assertEqual(u2.is_active, True)
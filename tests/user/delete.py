from django.shortcuts import reverse
from django.test import Client, TestCase

from user.models import User
from user.serializers import UserSerializer


class TestDeleteUser(TestCase):
  def test_delete_ok(self):
    u = User.objects.create(username="test_user", email="test@test.com")

    c = Client()
    resp = c.delete(reverse("api:users", kwargs={ "pk": u.id }))

    u.refresh_from_db()

    self.assertEqual(resp.status_code, 200)
    self.assertEqual(u.is_active, False)
from django.shortcuts import reverse
from django.test import TestCase


class TestGetSong(TestCase):
  @classmethod
  def setUpTestData(cls):
    cls.u = User.objects.create_user("test_user", "test@test.com")
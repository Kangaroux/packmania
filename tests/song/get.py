import os.path

from django.shortcuts import reverse
from django.test import TestCase

from lib.upload import load_songs_from_file


class TestGetSong(TestCase):
  @classmethod
  def setUpTestData(cls):
    cls.u = User.objects.create_user("test_user", "test@test.com")
    _, _, cls.songs = load_songs_from_file(os.path.join(settings.TEST_DATA_DIR, "abxy.zip"))
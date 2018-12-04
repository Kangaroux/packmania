import os
import unittest

from django.conf import settings
from django.shortcuts import reverse
from django.test import override_settings, TestCase

from song.models import Song
from song.serializers import SongSerializer
from user.models import User


class TestUploadSong(TestCase):
  @classmethod
  def setUpTestData(cls):
    cls.u = User.objects.create_user("test_user", "test@test.com")


  def test_not_logged_in(self):
    with open(os.path.join(settings.TEST_DATA_DIR, "abxy.zip"), "rb") as f:
      resp = self.client.post(reverse("api:songs"), { "file": f })

    self.assertEqual(resp.status_code, 401)

  def test_upload_ok(self):
    self.client.force_login(self.u)

    with open(os.path.join(settings.TEST_DATA_DIR, "abxy.zip"), "rb") as f:
      resp = self.client.post(reverse("api:songs"), { "file": f })

    self.assertEqual(resp.status_code, 200)

  @override_settings(MAX_UNCOMPRESSED_ZIP_SIZE=1024, TEXT_MAX_UNCOMPRESSED_ZIP_SIZE="1KB")
  def test_upload_file_too_big(self):
    self.client.force_login(self.u)

    with open(os.path.join(settings.TEST_DATA_DIR, "abxy.zip"), "rb") as f:
      resp = self.client.post(reverse("api:songs"), { "file": f })

    self.assertEqual(resp.status_code, 400)
    self.assertEqual(resp.json()["fields"]["file"], "The zip cannot be larger than 1KB when unzipped.")

  def test_upload_empty(self):
    self.client.force_login(self.u)

    with open(os.path.join(settings.TEST_DATA_DIR, "invalid_song_structure_5.zip"), "rb") as f:
      resp = self.client.post(reverse("api:songs"), { "file": f })

    self.assertEqual(resp.status_code, 400)
    self.assertEqual(resp.json()["fields"]["file"], "The zip cannot be empty.")

  def test_upload_invalid_file(self):
    self.client.force_login(self.u)

    with open(os.path.join(settings.TEST_DATA_DIR, "invalid_song_structure_6.zip"), "rb") as f:
      resp = self.client.post(reverse("api:songs"), { "file": f })

    self.assertEqual(resp.status_code, 400)
    self.assertEqual(resp.json()["fields"]["file"], "The zip cannot contain executables or other archives.")

  def test_upload_missing_files(self):
    self.client.force_login(self.u)

    with open(os.path.join(settings.TEST_DATA_DIR, "invalid_song_structure_7.zip"), "rb") as f:
      resp = self.client.post(reverse("api:songs"), { "file": f })

    self.assertEqual(resp.status_code, 400)
    self.assertEqual(resp.json()["fields"]["file"], "Zip archive needs to contain at least an audio and step file.")

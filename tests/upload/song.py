import json
import os
import unittest

from django.conf import settings
from django.shortcuts import reverse
from django.test import override_settings, TestCase
from rest_framework.renderers import JSONRenderer

from song.models import Song
from song.serializers import SongSerializer
from user.models import User


class TestUploadSong(TestCase):
  @classmethod
  def setUpTestData(cls):
    cls.u = User.objects.create_user("test_user", "test@test.com")


  def test_not_logged_in(self):
    with open(os.path.join(settings.TEST_DATA_DIR, "abxy.zip"), "rb") as f:
      resp = self.client.post(reverse("api:upload"), { "file": f })

    self.assertEqual(resp.status_code, 401)

  def test_upload_ok(self):
    self.client.force_login(self.u)

    with open(os.path.join(settings.TEST_DATA_DIR, "abxy.zip"), "rb") as f:
      resp = self.client.post(reverse("api:upload"), { "file": f })

    self.assertEqual(resp.status_code, 200)
    self.assertEqual(len(resp.json()["results"]), 1)
    self.assertEqual(resp.json()["results"], SongSerializer(Song.objects.all(), many=True).data)

  @override_settings(MAX_UNCOMPRESSED_ZIP_SIZE=1024, TEXT_MAX_UNCOMPRESSED_ZIP_SIZE="1KB")
  def test_upload_file_too_big(self):
    self.client.force_login(self.u)

    with open(os.path.join(settings.TEST_DATA_DIR, "abxy.zip"), "rb") as f:
      resp = self.client.post(reverse("api:upload"), { "file": f })

    self.assertEqual(resp.status_code, 400)
    self.assertEqual(resp.json()["fields"]["file"], "The zip cannot be larger than %s when unzipped."
      % settings.TEXT_MAX_UNCOMPRESSED_ZIP_SIZE)

  def test_upload_empty(self):
    self.client.force_login(self.u)

    with open(os.path.join(settings.TEST_DATA_DIR, "invalid_song_structure_5.zip"), "rb") as f:
      resp = self.client.post(reverse("api:upload"), { "file": f })

    self.assertEqual(resp.status_code, 400)
    self.assertEqual(resp.json()["fields"]["file"], "The zip file cannot be empty.")

  def test_upload_invalid_file(self):
    self.client.force_login(self.u)

    with open(os.path.join(settings.TEST_DATA_DIR, "invalid_song_structure_6.zip"), "rb") as f:
      resp = self.client.post(reverse("api:upload"), { "file": f })

    self.assertEqual(resp.status_code, 400)
    self.assertEqual(resp.json()["fields"]["file"], "The zip file contains blocked file types (such as: %s)."
      % ", ".join(settings.DISALLOWED_FILE_TYPES))

  def test_upload_missing_files(self):
    self.client.force_login(self.u)

    with open(os.path.join(settings.TEST_DATA_DIR, "invalid_song_structure_7.zip"), "rb") as f:
      resp = self.client.post(reverse("api:upload"), { "file": f })

    self.assertEqual(resp.status_code, 400)
    self.assertEqual(resp.json()["fields"]["file"], "Every song must have a valid step file.")

import os
import shutil
import time

from django.conf import settings
from django.core.files.base import File
from django.test import TestCase

from lib.parser.sm import SMParser
from lib.upload import *
from user.models import User


class TestSongUpload(TestCase):
  @classmethod
  def setUpTestData(cls):
    cls.u = User.objects.create_user("test_user", "test@test.com")

  @classmethod
  def setUpClass(cls):
    super().setUpClass()
    cls.dir = os.path.join("/tmp", "packmania")
    os.makedirs(cls.dir)

  @classmethod
  def tearDownClass(cls):
    super().tearDownClass()
    shutil.rmtree(cls.dir)


  def test_copy_public_file(self):
    src = os.path.join(self.dir, "test_file.foo")

    with open(src, "w") as f:
      pass

    self.assertEqual(copy_public_file(src), os.path.join(settings.MEDIA_ROOT, "test_file.foo"))
    self.assertEqual(copy_public_file(src, new_name="blah"), os.path.join(settings.MEDIA_ROOT, "blah"))
    self.assertEqual(copy_public_file(src, "foo/bar", new_name="blah"),
      os.path.join(settings.MEDIA_ROOT, "foo", "bar", "blah"))

  def test_create_song(self):
    parser = SMParser()
    parser.load_file(os.path.join(settings.TEST_DATA_DIR, "ABXY", "abxy.sm"))

    song = create_song(
      self.u,
      parser,
      os.path.join(settings.TEST_DATA_DIR, "abxy.zip"),
      os.path.join(settings.TEST_DATA_DIR, "ABXY", "abxy.ogg"),
      os.path.join(settings.TEST_DATA_DIR, "ABXY", "abxy-banner.png")
    )

    # Quick sanity check
    self.assertEqual(song.uploader, self.u)
    self.assertEqual(song.title, "ABXY")
    self.assertEqual(song.charts.count(), 4)

    # Verify URLs look right
    self.assertEqual(os.path.basename(song.banner_url), "banner.png")
    self.assertEqual(os.path.basename(song.download_url), "abxy.zip")
    self.assertEqual(os.path.basename(song.preview_url), "preview.ogg")

    self.assertTrue(song.banner_url.startswith(settings.MEDIA_ROOT))
    self.assertTrue(song.download_url.startswith(settings.MEDIA_ROOT))
    self.assertTrue(song.preview_url.startswith(settings.MEDIA_ROOT))

  def test_handle_song_upload(self):
    with open(os.path.join(settings.TEST_DATA_DIR, "abxy.zip"), "rb") as f:
      song = handle_song_upload(self.u, File(f, "abxy.zip"))

    self.assertEqual(song.uploader, self.u)
    self.assertEqual(song.title, "ABXY")
    self.assertEqual(song.charts.count(), 4)
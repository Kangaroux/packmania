import os
import shutil
import time
import unittest
import zipfile

from django.conf import settings
from django.core.files.base import File
from django.test import TestCase

from lib.zip_parser import ZipParser
from lib.step_parser.sm import SMParser
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
    dst = os.path.join(settings.MEDIA_ROOT, "test_file.foo")

    with open(src, "wb+") as f:
      f.write(b"hello1234")
      self.assertEqual(copy_public_file(f, "test_file.foo"), dst)

    with open(dst) as f:
      self.assertEqual(f.read(), "hello1234")

  @unittest.skip
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
    self.assertTrue(os.path.basename(song.banner_url).endswith(".png"))
    self.assertTrue(os.path.basename(song.download_url).endswith(".zip"))
    # self.assertTrue(os.path.basename(song.preview_url).endswith(".ogg"))

    self.assertTrue(song.banner_url.startswith(settings.MEDIA_ROOT))
    self.assertTrue(song.download_url.startswith(settings.MEDIA_ROOT))
    # self.assertTrue(song.preview_url.startswith(settings.MEDIA_ROOT))

  def test_extract_and_add_songs(self):
    with open(os.path.join(settings.TEST_DATA_DIR, "abxy.zip"), "rb") as f:
      zip_parser = ZipParser(f)

      with zip_parser:
        zip_parser.inspect()
        song = extract_and_add_songs(self.u, zip_parser)

    self.assertEqual(len(song), 1)
    self.assertEqual(song[0].uploader, self.u)
    self.assertEqual(song[0].title, "ABXY")
    self.assertEqual(song[0].charts.count(), 4)
import os
import shutil
import unittest

from django.conf import settings
from django.test import TestCase

from lib.upload import copy_public_file, copy_public_file_from_string
from user.models import User


class TestSongUpload(TestCase):
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
    dst = os.path.join(settings.MEDIA_ROOT, "test_copy_public_file.foo")

    with open(src, "wb+") as f:
      f.write(b"hello1234")
      self.assertEqual(copy_public_file(f, "test_copy_public_file.foo"), dst)

    with open(dst, "rb") as f:
      self.assertEqual(f.read(), b"hello1234")

    os.remove(dst)

  def test_copy_public_file_from_string(self):
    dst = os.path.join(settings.MEDIA_ROOT, "test_copy_public_file_from_string.foo")
    copy_public_file_from_string(b"testing 123", "test_copy_public_file_from_string.foo")

    with open(dst, "rb") as f:
      self.assertEqual(f.read(), b"testing 123")

    os.remove(dst)
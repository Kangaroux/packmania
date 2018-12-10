import os.path

from django.shortcuts import reverse
from django.test import TestCase

from lib.zip_parser import ZipParser


class TestGetSong(TestCase):
  @classmethod
  def setUpTestData(cls):
    cls.u = User.objects.create_user("test_user", "test@test.com")

  @classmethod
  def setUpClass(cls):
    super().setUpClass()
    cls.file = open(os.path.join(settings.TEST_DATA_DIR, "abxy.zip"))
    cls.zip_parser = ZipParser(cls.file)
    cls.zip_parser.inspect()

  @classmethod
  def tearDownClass(cls):
    cls.file.close()
    cls.tearDownClass()
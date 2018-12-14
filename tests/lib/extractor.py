import os.path
import re
import shutil
import unittest
from unittest.mock import MagicMock

from django.conf import settings
from django.test import TestCase

from lib.extract import SongExtractor
from lib.extract.extractor import ExtractedSong
from lib.zip_parser import ZipParser
from lib.step_parser.sm import SMParser
from lib.upload import *
from user.models import User


class TestExtractor(TestCase):
  @classmethod
  def setUpTestData(cls):
    cls.u = User.objects.create_user("test_user", "test@test.com")

  def test_banner_preview_dst_name(self):
    empty = ExtractedSong(None, None, None)

    # No banner or preview
    self.assertEqual(empty.get_preview_dst(), None)
    self.assertEqual(empty.get_banner_dst(), None)

    nonempty = ExtractedSong(None, "audio.mp3", MagicMock(filename="pic.png"))

    self.assertTrue(re.fullmatch(r'preview_.*\.mp3', nonempty.get_preview_dst()))
    self.assertTrue(re.fullmatch(r'banner_.*\.png', nonempty.get_banner_dst()))

  def test_extract_single_song(self):
    with open(os.path.join(settings.TEST_DATA_DIR, "abxy.zip"), "rb") as f:
      parsed_zip = ZipParser(f)

      with parsed_zip:
        parsed_zip.inspect()
        extractor = SongExtractor(parsed_zip, self.u)
        songs = extractor.extract_all()
        song = songs[0]

    # Quick sanity check
    self.assertEqual(len(songs), 1)
    self.assertEqual(song.title, "ABXY")

    self.assertTrue(os.path.basename(song.banner_url).endswith(".png"))
    self.assertTrue(os.path.basename(song.preview_url).endswith(".mp3"))
    self.assertTrue(os.path.basename(song.download_url).endswith(".zip"))

    # Cleanup dst folder
    shutil.rmtree(os.path.join(settings.MEDIA_ROOT, extractor.dst_folder))

  def test_extract_pack(self):
    with open(os.path.join(settings.TEST_DATA_DIR, "DDR 3rd Mix.zip"), "rb") as f:
      parsed_zip = ZipParser(f)

      with parsed_zip:
        parsed_zip.inspect()
        extractor = SongExtractor(parsed_zip, self.u)
        songs = extractor.extract_all()
        songs = sorted(songs, key=lambda x: x.title)

    # Quick sanity check
    self.assertEqual(len(songs), 3)
    self.assertEqual(songs[0].uploader, self.u)
    self.assertEqual(songs[0].title, "20,NOVEMBER (D.D.R. version)")
    self.assertEqual(songs[1].title, "AFRONOVA")
    self.assertEqual(songs[2].title, "BOOM BOOM DOLLAR (K.O.G G3 MIX)")

    for s in songs:
      self.assertTrue(os.path.basename(s.banner_url).endswith(".png"))
      self.assertTrue(os.path.basename(s.preview_url).endswith(".mp3"))
      self.assertTrue(os.path.basename(s.download_url).endswith(".zip"))

    # Cleanup dst folder
    shutil.rmtree(os.path.join(settings.MEDIA_ROOT, extractor.dst_folder))
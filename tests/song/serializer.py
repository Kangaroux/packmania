import re

from django.shortcuts import reverse
from django.test import TestCase

from lib.step_parser import BPM
from song.models import Song
from song.serializers import SongSerializer
from user.models import User


class TestSerializer(TestCase):
  @classmethod
  def setUpTestData(cls):
    cls.u = User.objects.create_user("test_user", "test@test.com")


  def test_serialize_song(self):
    data = {
      "uploader": self.u,
      "artist": "TestArtist",
      "author": "TestAuthor",
      "genre": "anime",
      "subtitle": "TestSubtitle",
      "title": "TestTitle",
      "has_stops": True,
      "bpm_type": BPM.RANDOM.value,
      "min_bpm": 123.0,
      "max_bpm": 456.0,
      "banner_url": "TestBanner.png",
      "download_url": "TestDownload.zip",
      "preview_url": "TestPreview.mp3",
    }

    song = Song.objects.create(**data)

    # Make some adjustments to match what it will look like when serialized
    data["id"] = song.id
    data["uploader"] = data["uploader"].id
    data["genre"] = "Anime"
    data["charts"] = []

    self.assertEqual(data, SongSerializer(song).data)
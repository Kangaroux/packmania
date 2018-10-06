import re

from django.shortcuts import reverse
from django.test import TestCase

from song.models import Song
from song.serializers import SongSerializer


# class TestSerializer(TestCase):
#   def test_serialize_song(self):
#     song = 
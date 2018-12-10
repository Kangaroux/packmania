from django.contrib.auth import login

from ..models import Song
from ..serializers import SongSerializer
from lib.api import APIView


class SongListAPI(APIView):
  """ Song API for getting collections of songs or uploading new ones """

  @staticmethod
  def serialize_songs(songs):
    return SongSerializer(songs, many=True).data

  def get(self, request, format=None):
    """ Gets a collection of songs """

    # TODO: Filtering, pagination
    return self.ok(self.serialize_songs(songs))


class SongDetailAPI(APIView):
  pass
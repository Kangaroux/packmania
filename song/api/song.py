from django.contrib.auth import login

from ..models import Song
from ..serializers import SongSerializer
from lib.api import APIView


class SongListAPI(APIView):
  """ Song API for getting collections of songs or uploading new ones """

  def get(self, request, format=None):
    """ Gets a collection of songs """

    # TODO: Filtering, pagination
    return self.ok(SongSerializer(Song.objects.all(), many=True).data)


class SongDetailAPI(APIView):
  pass
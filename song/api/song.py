from django.contrib.auth import login, logout

from ..forms import UploadSongForm
from ..models import Chart, Song
from ..serializers import SongSerializer
from lib.api import APIView
from lib.upload import handle_song_upload


class SongListAPI(APIView):
  """ Song API for getting collections of songs or uploading new ones """

  def get(self, request, format=None):
    """ Gets a collection of songs """

    # TODO: Filtering, pagination
    return self.ok(SongSerializer(Song.objects.all(), many=True).data)

  def post(self, request, format=None):
    """ Uploads a new song. Songs must be a zip file that contain a single folder
    which contains the files for one song.
    """
    if not request.user.is_authenticated:
      return self.not_logged_in()

    form = UploadSongForm(request.POST, request.FILES)

    if not form.is_valid():
      return self.form_error(form)

    handle_song_upload(request.user, request.FILES["file"])

    return self.ok()


class SongDetailAPI(APIView):
  pass
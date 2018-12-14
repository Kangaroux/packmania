from django.contrib.auth import login

from .song import SongListAPI
from ..forms import UploadForm
from lib.api import APIView
from lib.extract import ExtractError, SongExtractor


class UploadAPI(APIView):
  """ API for uploading songs/packs """

  def post(self, request, format=None):
    """ Accepts a zip file from the user that can be a song or a pack. If the upload
    was successful then returns the songs that were uploaded in the same format as
    calling GET /api/songs/
    """
    if not request.user.is_authenticated:
      return self.not_logged_in()

    form = UploadForm(request.POST, request.FILES, user=request.user)

    if not form.is_valid():
      return self.form_error(form)

    return self.ok(SongListAPI.serialize_songs(form.songs))
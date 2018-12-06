from django.contrib.auth import login

from ..forms import UploadForm
from lib.api import APIView
from lib.upload import handle_song_upload


class UploadAPI(APIView):
  """ API for uploading songs/packs """

  def post(self, request, format=None):
    """ Accepts a zip file from the user that can be a song or a pack """
    if not request.user.is_authenticated:
      return self.not_logged_in()

    form = UploadForm(request.POST, request.FILES)

    if not form.is_valid():
      return self.form_error(form)

    songs = handle_song_upload(request.user, request.FILES["file"], form.sm_files)

    return self.ok()
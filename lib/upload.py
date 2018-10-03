import os
import uuid
import zipfile

from django.conf import settings


def handle_song_upload(user, zip_file, step_file, audio_file):
  """ After the song has been uploaded and we've verified the zip looks safe,
  we need to do a few things:

  1. Parse the stepmania file
  2. Extract the banner (if there is one) and the song (which we'll trim to be a preview)
  3. Upload the files to Amazon S3 (when on production)
  4. Insert the song into the database
  """

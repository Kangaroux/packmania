from zipfile import BadZipFile, ZipFile

from django import forms
from django.conf import settings

from lib.song_parsers.zip import (
  contains_file_ext,
  get_songs,
  get_uncompressed_size,
  zip_as_tree,
  ZipParseException
)


class UploadForm(forms.Form):
  file = forms.FileField(max_length=settings.MAX_ZIP_SIZE, error_messages={
    "max_length": "File cannot be larger than %s." % settings.TEXT_MAX_ZIP_SIZE
  })

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    is_pack = False
    pack_name = None
    sm_files = []

  def clean_file(self):
    """ Inspects the zip to verify that:

    - It's a valid zip file
    - It won't be too big once decompressed
    - It doesn't contain any potentially malicious files
    - The folder structure of the song/pack is valid

    Also extracts some data from the zip file:

    - Is it a pack? If yes, what is its name?
    - What are the .sm files?
    """
    data = self.cleaned_data.get("file")

    if data:
      try:
        with ZipFile(data, "r") as f:
          tree = zip_as_tree(f)

          if get_uncompressed_size(tree) >= settings.MAX_UNCOMPRESSED_ZIP_SIZE:
            raise forms.ValidationError("The zip cannot be larger than %s when unzipped."
              % settings.TEXT_MAX_UNCOMPRESSED_ZIP_SIZE)
          elif contains_file_ext(tree, (".exe", ".zip", ".rar", ".7z")):
            # This doesn't have to be a complete list -- this is mostly just a
            # means of protecting us and the user from zip bombs
            raise forms.ValidationError("The zip cannot contain executables or other archives.")
          else:
            try:
              self.is_pack, self.pack_name, self.sm_files = get_songs(tree)
            except ZipParseException as e:
              raise forms.ValidationError(e)
      except BadZipFile:
        raise forms.ValidationError("File must be a valid ZIP.")

    return data
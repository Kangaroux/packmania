import zipfile

from django import forms
from django.conf import settings


class UploadSongForm(forms.Form):
  AUDIO_FILES = ("mp3", "wav", "ogg")
  STEP_FILES = ("sm", "ssc", "dwi")

  # Whitelist of valid file extensions. If we find a file that's not in this list the
  # song is rejected
  ALLOWED_FILE_EXT = (
    # Audio files
    *AUDIO_FILES,

    # Song files (we only officially support .sm)
    *STEP_FILES,
    "sm.old",
    "ssc.old",

    # Images
    "png",
    "jpg",
    "jpeg",
    "bmp",

    # Video backgrounds (rare)
    "mpg",
    "avi",

    # Text file
    "txt",
  )

  file = forms.FileField(max_length=settings.MAX_SONG_SIZE, error_messages={
    "max_length": "File cannot be larger than %s." % settings.MAX_SONG_SIZE_TEXT
  })

  def clean_file(self):
    """ Inspects the uploaded file
    """
    data = self.cleaned_data.get("file")

    if data:
      try:
        zf = zipfile.ZipFile(data)
        files = zf.infolist()
      except zipfile.BadZipFile:
        raise forms.ValidationError("File must be a zip containing a single song folder.")

      uncompressed_size = 0
      dir_name = None
      audio_file = False
      step_file = False

      if len(files) == 0:
        raise forms.ValidationError("Zip archive is empty.")

      # Inspect the zip before we try and extract it
      for file in files:
        if file.is_dir():
          continue

        file_path = file.filename.split("/")
        file_name = file_path[-1]

        if dir_name is None:
          dir_name = file_path[0]

        # Verify there is only one directory
        if len(file_path) != 2 or dir_name != file_path[0]:
          raise forms.ValidationError("Files should be contained in a single root folder.")

        ext = file_name.split(".", 1)

        # File doesn't have an extension
        if len(ext) == 1:
          raise forms.ValidationError("Invalid file found: %s" % file.filename)

        ext = ext[1].lower()
        ext_valid = False

        for allowed_ext in self.ALLOWED_FILE_EXT:
          if allowed_ext == ext:
            ext_valid = True

            if ext in self.AUDIO_FILES:
              audio_file = True
            elif ext in self.STEP_FILES:
              step_file = True

            break

        if not ext_valid:
          raise forms.ValidationError("Invalid file found: %s" % file.filename)

        uncompressed_size += file.file_size

      if not (audio_file and step_file):
        raise forms.ValidationError("Zip archive needs to contain at least an audio and step file.")

      if uncompressed_size > settings.MAX_SONG_SIZE_UNZIPPED:
        raise forms.ValidationError("File cannot be larger than %s when unzipped."
          % settings.MAX_SONG_SIZE_UNZIPPED_TEXT)

    return data
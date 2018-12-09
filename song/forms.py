import logging

from django import forms
from django.conf import settings

from lib.zip_parser import BaseZipError, ZipParser


logger = logging.getLogger(__file__)


class UploadForm(forms.Form):
  file = forms.FileField(max_length=settings.MAX_ZIP_SIZE, error_messages={
    "max_length": "File cannot be larger than %s." % settings.TEXT_MAX_ZIP_SIZE
  })

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    zip_parser = None

  def clean_file(self):
    """ Inspects the zip file to see if it's valid """
    zip_file = self.cleaned_data.get("file")

    if zip_file:
      self.zip_parser = ZipParser(zip_file)

      try:
        with self.zip_parser:
          self.zip_parser.inspect(settings.MAX_UNCOMPRESSED_ZIP_SIZE, settings.DISALLOWED_FILE_EXTENSIONS)
      except BaseZipError as e:
        raise forms.ValidationError(e)
      except Exception as e:
        logger.exception("Error when trying to inspect zip file")
        raise forms.ValidationError("An unexpected error occurred when inspecting the zip file.")

    return zip_file
import io
import logging
import os
import os.path

from django.conf import settings


logger = logging.getLogger(__name__)


def copy_public_file(data, dst_path, is_file=True):
  """ Copies `data` to `dst_path` which is in a publically accessible folder.
  `data` should either be an open file object, or the actual file contents,
  in which case `is_file` should be False.

  For development this copies the file to a public folder, on production this
  copies the file to S3
  """
  new_uri = ""

  if settings.DEV:
    new_uri = os.path.join(settings.MEDIA_ROOT, dst_path)
    os.makedirs(os.path.dirname(new_uri), exist_ok=True)

    with open(new_uri, "wb") as dst:
      if is_file:
        try:
          data.seek(0)
        except io.UnsupportedOperation:
          pass

        while True:
          # Copy the file over 1MB at a time
          chunk = data.read(2**20)
          dst.write(chunk)

          # EOF
          if len(chunk) < 2**20:
            break
      else:
        dst.write(data)
  else:
    # TODO
    pass

  return new_uri


def copy_public_file_from_string(data, dst_path):
  return copy_public_file(data, dst_path, is_file=False)
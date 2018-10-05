import logging
import os
import os.path
import shutil
import uuid
import zipfile

from django.conf import settings
from django.core.files.base import File

from lib import util
from lib.parser.sm import SMParser
from song.models import Chart, Song


logger = logging.getLogger(__name__)


def copy_public_file(file, dst="", new_name=None):
  """ Copies `file` to `dst` where `dst` is a publicly viewable directory for hosting
  user files. On dev this is MEDIA_ROOT, and on prod this is an S3 bucket. Returns the
  full uploaded URI of the file.

  `file` should be either a file path or a django File object
  """
  new_uri = ""

  if isinstance(file, File):
    file_name = file.name
  else:
    file_name = os.path.basename(file)

  if settings.DEV:
    new_uri = os.path.join(settings.MEDIA_ROOT, dst, new_name if new_name else file_name)

    os.makedirs(os.path.dirname(new_uri), exist_ok=True)

    if isinstance(file, File):
      with open(new_uri, "wb") as dst_file:
        for chunk in file.chunks():
          try:
            dst_file.write(chunk)
          except TypeError:
            dst_file.write(chunk.encode("utf-8"))
    else:
      shutil.copyfile(file, new_uri)
  else:
    # TODO
    pass

  return new_uri


def handle_song_upload(user, zip_file):
  """ Creates a new song and chart(s) from a user uploaded zip file. `zip_file` must be
  an instance of django.core.files.base.File
  """
  zf = zipfile.ZipFile(zip_file)
  tmp_dir = os.path.join(settings.TMP_DIR, str(uuid.uuid1()))
  song = None

  # Create a temp dir we can extract the files to
  os.makedirs(tmp_dir)

  # Extract the step file
  step_file = zf.extract(
    util.first(zf.namelist(), lambda x: x.endswith(".sm"))[0],
    tmp_dir
  )

  try:
    # Parse the step file
    parser = SMParser()
    parser.load_file(step_file)

    # Extract the audio file
    audio_file = zf.extract(
      util.first(zf.namelist(), lambda x: os.path.basename(x) == parser.song.file_name)[0],
      tmp_dir
    )

    # Extract the banner file (if it exists)
    if parser.display.banner:
      banner_file = zf.extract(
        util.first(zf.namelist(), lambda x: os.path.basename(x) == parser.display.banner)[0],
        tmp_dir
      )
    else:
      banner_file = None

    create_preview(parser.song.preview_start, parser.song.preview_length, audio_file)
    song = create_song(user, parser, zip_file, audio_file, banner_file)
  except Exception as e:
    logger.exception("Exception occurred while processing uploaded song")
  finally:
    shutil.rmtree(tmp_dir)

  return song


def create_preview(start, length, audio_file):
  """ Trims the audio file down to create a preview version """
  pass


def create_song(user, data, zip_file, audio_file, banner_file):
  dst = str(uuid.uuid1())

  zip_file = copy_public_file(zip_file, dst)
  audio_file = copy_public_file(audio_file, dst, new_name=util.rename_file(audio_file, "preview"))

  if banner_file:
    banner_file = copy_public_file(banner_file, dst, new_name=util.rename_file(banner_file, "banner"))
  else:
    banner_file = None

  # Create a new Song instance
  song = Song.objects.create(
    uploader=user,
    artist=data.display.artist,
    author=data.display.author,
    subtitle=data.display.subtitle,
    title=data.display.title,

    # TODO: Try and match the genre
    # genre=data.display.genre,

    has_stops=data.song.has_stops,
    bpm_type=data.song.bpm_type.value,
    min_bpm=data.song.bpm_range[0],
    max_bpm=data.song.bpm_range[1],

    download_url=zip_file,
    preview_url=audio_file,
    banner_url=banner_file
  )

  # Bulk insert the charts for the song
  Chart.objects.bulk_create([
    Chart(
      type=chart.type,
      meter=chart.meter,
      difficulty=chart.difficulty,

      fakes=chart.steps.fakes,
      hands=chart.steps.hands,
      holds=chart.steps.holds,
      jumps=chart.steps.jumps,
      lifts=chart.steps.lifts,
      mines=chart.steps.mines,
      rolls=chart.steps.rolls,
      taps=chart.steps.taps,

      song=song
    ) for chart in data.charts
  ])

  return song
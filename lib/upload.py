import logging
import os
import os.path
import shutil
import uuid
import zipfile

from django.conf import settings

from lib import util
from lib.parser.sm import SMParser
from song.models import Chart, Song


logger = logging.getLogger(__name__)


def copy_public_file(file, dst, new_name=None):
  """ Copies `file` to `dst` where `dst` is a publicly viewable directory for hosting
  user files. On dev this is MEDIA_ROOT, and on prod this is an S3 bucket. Returns the
  full uploaded URI of the file
  """
  new_uri = ""
  file_dir = os.path.dirname(file)
  file_name = os.path.basename(file) if not new_name else new_name

  if settings.DEV:
    new_uri = os.path.join(settings.MEDIA_ROOT, dst, file_dir, file_name)
    os.makedirs(os.path.dirname(new_uri))

    with open(file, "r") as src_file, open(new_uri, "w") as dst_file:
      for chunk in src_file.chunks():
        dst_file.write(chunk)
  else:
    # TODO
    pass

  return new_uri


def handle_song_upload(user, zip_file):
  """ Creates a new song and chart(s) from a user uploaded zip file """
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
    song = create_song(user, zip_file, parser, audio_file, banner_file)
  except Exception as e:
    logger.exception("Exception occurred while processing uploaded song")
  finally:
    shutil.rmtree(tmp_dir)

  return song


def create_preview(start, length, audio_file):
  """ Trims the audio file down to create a preview version """
  pass


def create_song(user, zip_file, data, audio_file, banner_file):
  dst = str(uuid.uuid1())

  zip_file = copy_public_file(zip_file, dst)
  audio_file = copy_public_file(audio_file, dst, new_name=util.rename_file(audio_file, "preview"))

  if banner_file:
    banner_file = copy_public_file(banner_file, dst, new_name=util.rename_file(banner_file, "banner"))

  # Create a new Song instance
  song = Song.objects.create(
    uploader=user,
    artist=parser.display.artist,
    author=parser.display.author,
    subtitle=parser.display.subtitle,
    title=parser.display.title,

    # TODO: Try and match the genre
    # genre=parser.display.genre,

    has_stops=parser.song.has_stops,
    bpm_type=parser.song.bpm_type.value,
    min_bpm=parser.song.bpm_range[0],
    max_bpm=parser.song.bpm_range[1],

    download_url=new_uris[0],
    preview_url=new_uris[1],
    banner_url=new_uris[2] if banner_file else None
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
    ) for chart in parser.charts
  ])

  return song
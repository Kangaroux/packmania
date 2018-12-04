import io
import logging
import os
import os.path
import uuid
import zipfile

from django.conf import settings
from django.core.files.base import File

from lib import util
from lib.parser.sm import SMParser
from song.models import Chart, Song


logger = logging.getLogger(__name__)


class UploadError(Exception):
  pass


def copy_public_file(file, dst_path):
  """ Writes a file to a publically accessible folder

  For development this copies the file to a public folder, on production this
  copies the file to S3
  """
  new_uri = ""

  if settings.DEV:
    new_uri = os.path.join(settings.MEDIA_ROOT, dst_path)
    os.makedirs(os.path.dirname(new_uri), exist_ok=True)

    with open(new_uri, "wb") as dst:
      # Because we're accepting a file object as an argument we don't know how
      # long it's been open, so try resetting it back to the beginning of the file
      try:
        file.seek(0)
      except io.UnsupportedOperation:
        pass

      while True:
        # Copy the file over 1MB at a time
        chunk = file.read(2**20)
        dst.write(chunk)

        # EOF
        if len(chunk) < 2**20:
          break
  else:
    # TODO
    pass

  return new_uri


def get_file_from_zip(zip_file, path):
  try:
    return zip_file.getinfo(path)
  except KeyError:
    return None


def handle_song_upload(user, uploaded_file, step_files):
  """ Reads the .sm files in the zip to extract the audio and banner, as well as
  create songs and charts in the database.

  Returns a list of Songs inserted into the database, or raises an UploadError
  if something went wrong
  """
  songs = []

  with zipfile.ZipFile(uploaded_file, "r") as zip_file:
    parsed_step_files = []
    audio_files = []
    banner_files = []

    # Parse the step files to verify that the file is valid
    for sf in step_files:
      parser = SMParser()
      parsed_step_files.append(parser)

      try:
        # Load the step file into memory and parse it
        with zip_file.open(sf) as f:
          parser.load_from_string(f.read())
      except Exception as e:
        logger.exception("Error while parsing step file")
        raise UploadError("The file '%s' could not be parsed, it may be corrupted "
          "or an unsupported format." % sf.filename)

    # Look up the assets for each file
    for i in range(len(step_files)):
      sf = step_files[i]
      parser = parsed_step_files[i]
      base_path = sf.filename.rsplit("/", 1)[0]
      audio_path = "/".join([ base_path, parser.song.file_name ])
      audio_file = get_file_from_zip(zip_file, audio_path)

      # Audio file doesn't exist
      if not audio_file:
        raise UploadError("The audio file '%s' for song '%s' does not exist."
          % (parser.song.file_name, sf.filename))

      banner_file = None

      # Get the banner
      if parser.display.banner:
        banner_file = get_file_from_zip(zip_file, "/".join([ base_path, parser.display.banner ]))

        # Doesn't exist, ignore
        if not banner_file:
          logger.warning("Banner '%s' does not exist, ignoring..." % banner_file)

      audio_files.append(audio_file)
      banner_files.append(banner_file)

    # Get a unique alphanumeric for the folder name
    dst_folder = uuid.uuid4().hex
    zip_dst = os.path.join(dst_folder, "upload.zip")
    banner_dst = []

    # Copy the zip file
    copy_public_file(uploaded_file, zip_dst)

    # Copy the banners
    for b in banner_files:
      if not b:
        banner_dst.append(None)
        continue

      with zip_file.open(b) as f:
        name = os.path.join(dst_folder, "banner%s.%s" % (uuid.uuid4().hex, b.filename.split(".", 1)[1]))
        banner_dst.append(name)
        copy_public_file(f, name)

    # Insert the songs/charts into the database
    for i in range(len(parsed_step_files)):
      songs.append(create_song(user, parsed_step_files[i], zip_dst, None, banner_dst[i]))

  return songs


def create_preview(start, length, audio_file):
  """ Trims the audio file down to create a preview version.
  TODO: Use ffmpeg
  """
  pass


def create_song(user, data, zip_path, audio_path, banner_path):
  """ Creates a new song in the database """
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

    download_url=zip_path,
    preview_url=audio_path,
    banner_url=banner_path
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
import logging
import os
import shutil
import uuid
import zipfile

from django.conf import settings

from lib.parser.sm import SMParser
from song.models import Chart, Song


logger = logging.getLogger(__name__)


def handle_song_upload(user, zip_file, step_file, audio_file):
  """ After the song has been uploaded and we've verified the zip looks safe,
  we need to do a few things:

  1. Parse the stepmania file
  2. Extract the banner (if there is one) and the song (which we'll trim to be a preview)
  3. Upload the files to Amazon S3 (when on production)
  4. Insert the song into the database

  Returns the new Song instance, or None if it was unsuccessful
  """
  song = None
  zf = zipfile.ZipFile(zip_file)
  tmp_dir = os.path.join(settings.TMP_DIR, str(uuid.uuid1()))

  # Create a temp dir we can extract the files to
  os.makedirs(tmp_dir)

  # Extract the step file
  # TODO: Extract and trim audio file to generate preview
  step_file_path = zf.extract(step_file, tmp_dir)

  try:
    # Parse the step file
    parser = SMParser()
    parser.load_file(os.path.join(tmp_dir, step_file.filename))

    # Create a new Song instance
    song = Song(
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

      banner_url="",
      preview_url=""
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

  except Exception as e:
    logger.exception("Exception occurred while processing uploaded song")
  finally:
    shutil.rmtree(tmp_dir)

  return song
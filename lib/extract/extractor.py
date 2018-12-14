import logging
import os.path
import subprocess
import tempfile

from django.conf import settings

from .exceptions import MissingAudioFileError, StepFileParseError
from lib import util
from lib.step_parser.sm import SMParser
from lib.upload import copy_public_file, copy_public_file_from_string
from song.models import Chart, Song


logger = logging.getLogger(__name__)


class ExtractedSong:
  """ Represents a song that has been "extracted" from the zip and parsed """

  def __init__(self, song_data, preview_file_path, banner_file):
    self.song_data = song_data
    self.preview_file_path = preview_file_path
    self.banner_file = banner_file

    # The names that the files will have once uploaded to the public server
    self.preview_dst = None
    self.banner_dst = None

  def get_preview_dst(self):
    """ Returns the public name of the audio preview (or None if there was an error
    creating the preview)
    """
    if not self.preview_file_path:
      return None

    if not self.preview_dst:
      self.preview_dst = "preview_%s.mp3" % util.random_hex_string(8)

    return self.preview_dst

  def get_banner_dst(self):
    """ Returns the public name of the banner (or None if there is no banner) """
    if not self.banner_file:
      return None

    if not self.banner_dst:
      self.banner_dst = "banner_%s.%s" % (
        util.random_hex_string(8),
        os.path.basename(self.banner_file.filename).rsplit(".", 1)[1]
      )

    return self.banner_dst


class SongExtractor:
  """ Extractor for reading step files from a parsed zip file. Inserts the songs
  into the database and copies the files to a public folder
  """

  def __init__(self, parsed_zip, user):
    self.parsed_zip = parsed_zip
    self.user = user
    self.extracted_songs = []

    # The destination folder for the song(s)
    self.dst_folder = util.random_hex_string(16)
    self.zip_name = ""

  def extract_all(self):
    """ Extracts all of the songs from the zip, uploads the zip and song assets to
    a public folder, adds the songs to the db, and then returns all of the song
    instances added to the db
    """
    songs = []

    # Extract and parse the step files. It's important that we parse all of the step
    # files first in case we encounter an error, otherwise we'd need to backtrack
    for sf in self.parsed_zip.step_files:
      self.extracted_songs.append(self._read_song(sf))

    self._copy_zip_to_public_folder()

    # Copy the song assets (preview, banner) to the public folder and add the song
    # to the database
    for ex in self.extracted_songs:
      self._copy_song_to_public_folder(ex)
      songs.append(self._add_song_to_db(ex))

    return songs

  def _create_audio_preview(self, step_parser, audio_file):
    """ Extracts the audio file and trims it using ffmpeg to produce a trimmed
    mp3 file. If the preview was created successfully, returns the file path,
    otherwise None
    """
    if not audio_file:
      return None

    # Extracted audio file path
    ex_path = os.path.join(settings.TMP_DIR, "%s_%s" % (util.random_hex_string(16), step_parser.song.file_name))

    # Extract the file
    with open(ex_path, "wb") as ex:
      ex.write(self.parsed_zip.zf.read(audio_file))

    preview_path = os.path.join(settings.TMP_DIR, "%s_preview.mp3" % ex_path)

    try:
      # Try to create the preview using ffmpeg
      subprocess.run("%s -ss %f -t %f -i '%s' -ab %s -ac 2 '%s' -y -v error" % (
        settings.FFMPEG_PATH,
        step_parser.song.preview_start,
        min(step_parser.song.preview_length, settings.PREVIEW_MAX_LENGTH),
        ex_path,
        settings.PREVIEW_BITRATE,
        preview_path
      ), shell=True)
    except subprocess.CalledProcessError:
      logger.warning("ffmpeg returned non-zero status for '%s'" % step_parser.song.file_name)
      return None

    # Remove the extracted file
    os.remove(ex_path)

    return preview_path

  def _get_file_from_zip(self, path):
    """ Returns a file in the zip or None if it doesn't exist """
    try:
      return self.parsed_zip.zf.getinfo(path)
    except KeyError:
      return None

  def _read_song(self, step_file):
    """ Reads the given step file and returns an ExtractedSong object """
    step_parser = SMParser()
    step_file_name = os.path.basename(step_file.filename)

    try:
      # Load the step file into memory and parse it
      with self.parsed_zip.zf.open(step_file) as f:
        step_parser.load_from_string(f.read())
    except Exception as e:
      logger.exception("Error while parsing step file")
      raise StepFileParseError("The step file '%s' could not be parsed, it may be corrupted "
        "or an unsupported format." % step_file_name)

    # Step file does not define an audio file
    if not step_parser.song.file_name:
      raise MissingAudioFileError("The song '%s' does not have an audio file." % step_file_name)

    dir_name = os.path.dirname(step_file.filename)
    audio_file = self._get_file_from_zip(os.path.join(dir_name, step_parser.song.file_name))

    # Audio file doesn't exist
    if not audio_file:
      print(os.path.join(dir_name, step_parser.song.file_name))
      print(self.parsed_zip.zf.namelist())
      raise MissingAudioFileError("The audio file '%s' for song '%s' does not exist." % (
        step_parser.song.file_name,
        step_file_name)
      )

    preview_file_path = self._create_audio_preview(step_parser, audio_file)
    banner_file = None

    # Get the banner if it exists
    if step_parser.display.banner:
      banner_file = self._get_file_from_zip(os.path.join(dir_name, step_parser.display.banner))

      # Doesn't exist, ignore
      if not banner_file:
        logger.warning("Banner '%s' does not exist, ignoring..." % step_parser.display.banner)

    return ExtractedSong(step_parser, preview_file_path, banner_file)

  def _copy_zip_to_public_folder(self):
    """ Copies the zip file to the public folder """
    # If this is a single song then make the zip "artist - title.zip"
    if len(self.extracted_songs) == 1:
      self.zip_name = "%s - %s.zip" % (
        self.extracted_songs[0].song_data.display.artist,
        self.extracted_songs[0].song_data.display.title
      )
    elif self.parsed_zip.pack_name:
      self.zip_name = "%s.zip" % self.parsed_zip.pack_name
    else:
      self.zip_name = "upload.zip"

    copy_public_file(self.parsed_zip.file, os.path.join(self.dst_folder, self.zip_name))

  def _copy_song_to_public_folder(self, song):
    """ Copies the audio preview and banner to a public folder """
    banner_dst = song.get_banner_dst()
    preview_dst = song.get_preview_dst()

    # Copy the banner
    if banner_dst:
      with self.parsed_zip.zf.open(song.banner_file) as f:
        copy_public_file_from_string(f.read(), os.path.join(self.dst_folder, banner_dst))

    # Copy the preview
    if preview_dst:
      with open(song.preview_file_path, "rb") as f:
        copy_public_file_from_string(f.read(), os.path.join(self.dst_folder, preview_dst))

      # We no longer need a local copy of the preview
      os.remove(song.preview_file_path)

  def _add_song_to_db(self, song):
    """ Adds the song to the database and returns it """
    data = song.song_data

    db_song = Song.objects.create(
      uploader=self.user,
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

      # download_url=zip_path,
      preview_url=song.get_preview_dst(),
      banner_url=song.get_banner_dst(),
      download_url=self.zip_name
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

        song=db_song
      ) for chart in data.charts
    ])

    return db_song

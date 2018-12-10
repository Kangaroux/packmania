import io
import logging
import os
import os.path

from django.conf import settings
from django.core.files.base import File

from lib import util
from lib.step_parser.sm import SMParser
from lib.upload import copy_public_file
from song.models import Chart, Song


logger = logging.getLogger(__name__)


class ExtractedSong:
  """ Represents a song that has been "extracted" from the zip and parsed """

  def __init__(self, song_data, audio_file, banner_file):
    self.song_data = song_data
    self.audio_file = audio_file
    self.banner_file = banner_file

    # The names that the files will have once uploaded to the public server
    self.preview_dst = None
    self.banner_dst = None

  def get_preview_dst(self):
    """ Returns the public name of the audio preview """
    if not self.preview_dst:
      self.preview_dst = "preview_%s.%s" % (
        util.random_hex_string(8),
        os.path.basename(self.audio_file.filename).split(".", 1)[1]
      )

    return self.preview_dst

  def get_banner_dst(self):
    """ Returns the public name of the banner (or None if there is no banner) """
    if not self.banner_file:
      return None

    if not self.banner_dst:
      self.banner_dst = "banner_%s.%s" % (
        util.random_hex_string(8),
        os.path.basename(self.banner_file.filename).split(".", 1)[1]
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

  def extract_all(self):
    """ Extracts all of the songs from the zip, uploads the zip and song assets to
    a public folder, adds the songs to the db, and then returns all of the song
    instances added to the db
    """
    songs = []

    # Extract and parse the step files. It's important that we parse all of the step
    # files first in case we encounter an error, otherwise we'd need to backtrack
    for sf in parsed_zip.step_files:
      self.extracted_songs.append(self._read_song(sf))

    self._copy_zip_to_public_folder()

    # Copy the song assets (preview, banner) to the public folder and add the song
    # to the database
    for ex in self.extracted_songs:
      self._copy_song_to_public_folder(ex)
      songs.append(self._add_song_to_db(ex))

    return songs

  def _get_file_from_zip(self, path):
    """ Returns a file in the zip or None if it doesn't exist """
    try:
      return self.parsed_zip.zf.getinfo(path)
    except KeyError:
      return None

  def _read_song(self, step_file):
    """ Reads the given step file and returns an ExtractedSong object """
    parser = SMParser()
    step_file_name = os.path.basename(step_file.filename)

    try:
      # Load the step file into memory and parse it
      with self.parsed_zip.zf.open(step_file) as f:
        parser.load_from_string(f.read())
    except Exception as e:
      logger.exception("Error while parsing step file")
      raise StepFileParseError("The step file '%s' could not be parsed, it may be corrupted "
        "or an unsupported format." % step_file_name)

    # Step file does not define an audio file
    if not parser.song.file_name:
      raise MissingAudioFileError("The song '%s' does not have an audio file." % step_file_name)

    dir_name = os.path.dirname(step_file.filename)
    audio_file = self._get_file_from_zip(os.path.join(dir_name, parser.song.file_name))

    # Audio file doesn't exist
    if not audio_file:
      raise MissingAudioFileError("The audio file '%s' for song '%s' does not exist." % (
        parser.song.file_name,
        step_file_name)
      )

    banner_file = None

    # Get the banner if it exists
    if parser.display.banner:
      banner_file = self._get_file_from_zip(os.path.join(dir_name, parser.display.banner))

      # Doesn't exist, ignore
      if not banner_file:
        logger.warning("Banner '%s' does not exist, ignoring..." % banner_file)

    return ExtractedSong(parser, audio_file, banner_file)

  def _copy_zip_to_public_folder(self):
    """ Copies the zip file to the public folder """
    zip_name = ""

    # If this is a single song then make the zip "artist - title.zip"
    if len(self.extracted_songs) == 1:
      zip_name = "%s - %s.zip" % (
        self.extracted_songs[0].song_data.display.artist,
        self.extracted_songs[0].song_data.display.title
      )
    elif self.parsed_zip.pack_name:
      zip_name = "%s.zip" % self.parsed_zip.pack_name
    else:
      zip_name = "upload.zip"

  def _copy_song_to_public_folder(self, song):
    """ Copies the audio preview and banner to a public folder """
    # TODO

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
      banner_url=song.get_banner_dst()
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

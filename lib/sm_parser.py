from enum import Enum


class StepInfo:
  """ Information about the song's chart """

  class Type(Enum):
    EMPTY = "0"
    TAP = "1"
    HOLD = "2"
    HOLD_ROLL_END = "3"
    ROLL = "4"
    MINE = "M"
    LIFT = "L"
    FAKE = "F"

  def __init__(self):
    self.taps = 0
    self.holds = 0
    self.rolls = 0
    self.mines = 0
    self.lifts = 0
    self.fakes = 0
    self.jumps = 0
    self.hands = 0
    self.quads = 0


class ChartInfo:
  """ Information for each difficulty """

  class Type(Enum):
    SINGLE = "dance-single"
    DOUBLE = "dance-double"
    # SOLO = "dance-solo"
    # THREEPANEL = "dance-threepanel"
    # ROUTINE = "dance-routine"

  class Difficulty(Enum):
    NOVICE = "Beginner"
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"
    EXPERT = "Challenger"
    EDIT = "Edit"

    @classmethod
    def convert(cls, name):
      name = name.lower()
      difficulty_map = {
        "beginner": cls.NOVICE,
        "easy": cls.EASY,
        "basic": cls.EASY,
        "light": cls.EASY,
        "medium": cls.MEDIUM,
        "another": cls.MEDIUM,
        "trick": cls.MEDIUM,
        "standard": cls.MEDIUM,
        "difficult": cls.MEDIUM,
        "hard": cls.HARD,
        "ssr": cls.HARD,
        "maniac": cls.HARD,
        "heavy": cls.HARD,
        "smaniac": cls.EXPERT,
        "challenge": cls.EXPERT,
        "expert": cls.EXPERT,
        "oni": cls.EXPERT,
        "edit": cls.EDIT,
      }

      return difficulty_map.get(name)


  def __init__(self):
    self.chart_type = None
    self.meter = 1
    self.difficulty = None
    self.steps = StepInfo()


class DisplayInfo:
  """ Information used for displaying the song """

  def __init__(self):
    self.artist = ""
    self.author = ""
    self.background = ""
    self.banner = ""
    self.genre = ""
    self.subtitle = ""
    self.title = ""


class SongInfo:
  """ Information about the song itself """

  def __init__(self):
    self.file_name = ""
    self.preview_start = 0
    self.preview_length = 0
    self.random_bpm = False
    self.bpm_range = (60, 60)
    self.has_stops = False


class SMParser:
  """ Parser for .sm files. Extracts information such as the song name, BPM,
  tap/hold counts, etc.

  This parser is based off the official stepmania .sm file parser:
  https://github.com/stepmania/stepmania/blob/master/src/NotesLoaderSM.cpp
  """

  def __init__(self):
    self.charts = []
    self.display = DisplayInfo()
    self.song = SongInfo()

  def load_file(self, file_path):
    """ Loads step information from a file. Returns True/False based on whether the song
    could be parsed successfully
    """
    with open(file_path, "r") as f:
      s = f.read()

    return self.load_from_string(s)

  def load_from_string(self, s):
    """ Loads step information from a string. Returns True/False based on whether the song
    could be parsed successfully
    """
    data = self.parse(s)

  def parse(self, s):
    """ Simple state-based parser to extract the tags and values from the SM file """
    STARTOFTAG = 0
    TAGNAME = 1
    TAGDATA = 2

    name = ""
    value = ""
    state = STARTOFTAG
    row = 1
    col = 0
    comment = False

    for i in range(len(s)):
      c = s[i]
      col += 1

      if c == "\n":
        row += 1
        col = 0
        comment = False
        continue
      elif c == "/" and s[i + 1] == "/":
        comment = True
      elif c == " " and name == "NOTES" and state == TAGDATA:
        continue

      if comment:
        continue

      if state == STARTOFTAG:
        if c != "#":
          raise Exception("Expected '#' on row %d col %d" % (row, col))
        else:
          state = TAGNAME
      elif state == TAGNAME:
        if c != ":":
          name += c
        else:
          state = TAGDATA
      elif state == TAGDATA:
        if c != ";":
          value += c
        else:
          self.handle_tag(name, value)
          state = STARTOFTAG
          name = ""
          value = ""

  def handle_tag(self, name, value):
    name = name.strip()
    value = value.strip()

    if name == "TITLE":
      self.display.title = value
    elif name == "SUBTITLE":
      self.display.subtitle = value
    elif name == "ARTIST":
      self.display.artist = value
    elif name == "BACKGROUND":
      self.display.background = value
    elif name == "BANNER":
      self.display.banner = value
    elif name == "GENRE":
      self.display.genre = value
    elif name == "CREDIT":
      self.display.author = value
    elif name == "MUSIC":
      self.song.file_name = value
    elif name == "DISPLAYBPM":
      if value == "*":
        self.song.random_bpm = True
      else:
        bpm = value.split(":")

        if len(bpm) == 1:
          bpm = float(bpm)
          self.song.bpm_range = (bpm, bpm)
        elif len(bpm) == 2:
          self.song.bpm_range = (float(bpm[0]), float(bpm[1]))
    elif name == "SAMPLESTART":
      self.song.preview_start = float(value)
    elif name == "SAMPLELENGTH":
      self.song.preview_length = float(value)
    elif name == "STOPS":
      self.song.has_stops = len(value) > 0
    elif name == "NOTES":
      self.parse_chart(value)

  def parse_chart(self, note_data):
    """ Parses the metadata from a chart and adds it to the chart list """
    note_data = note_data.split(":")
    chart = ChartInfo()

    # Strip the metadata fields
    for i in range(len(note_data) - 1):
      note_data[i] = note_data[i].strip()

    try:
      chart.chart_type = ChartInfo.Type(note_data[0])
    except ValueError:
      print("Unsupported chart type '%s', skipping..." % note_data[0])
      return

    chart.difficulty = ChartInfo.Difficulty.convert(note_data[2])
    chart.meter = int(note_data[3])

    # TODO: Handle parsing charts for doubles
    if chart.chart_type == ChartInfo.Type.SINGLE:
      self.parse_notes(chart, note_data[5])

    self.charts.append(chart)

  def parse_notes(self, chart, notes):
    """ Parses the notes for a song """
    row = ""

    for n in notes:
      if n == ",":
        row = ""
        continue

      row += n

      # TODO: Handle charts that aren't 4 key
      if len(row) == 4:
        consecutive_taps = 0

        # Parse each step
        for b in row:
          if b == StepInfo.Type.MINE:
            chart.steps.mines += 1
          elif b == StepInfo.Type.LIFT:
            chart.steps.lifts += 1
          elif b == StepInfo.Type.FAKE:
            chart.steps.fakes += 1
          elif b == StepInfo.Type.TAP:
            consecutive_taps += 1
          elif b == StepInfo.Type.HOLD:
            consecutive_taps += 1
            chart.steps.holds += 1
          elif b == StepInfo.Type.ROLL:
            consecutive_taps += 1
            chart.steps.rolls += 1

        # Handle how many directions have to be pressed at once
        if consecutive_taps == 1:
          chart.steps.taps += 1
        elif consecutive_taps == 2:
          chart.steps.jumps += 1
        elif consecutive_taps == 3:
          chart.steps.hands += 1
        elif consecutive_taps == 4:
          chart.steps.quads += 1

        row = ""
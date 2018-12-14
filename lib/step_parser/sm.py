from .base import *


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
    """ Loads step information from a file """
    with open(file_path, "r") as f:
      s = f.read()

    self.load_from_string(s)

  def load_from_string(self, s):
    """ Loads step information from a string """
    self.parse(s)

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

    if isinstance(s, bytes):
      s = s.decode("utf-8")

    # .sm files use the format: #<TAG_NAME>:[tag_value];
    for i in range(len(s)):
      c = s[i]
      col += 1

      if c == "\r":
        continue
      elif c == "\n":
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
    """ Parses a name/value pair """
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
    elif name == "BPMS":
      # DISPLAYBPM takes priority over this, so only set the range if we haven't already
      if self.song.bpm_range is None:
        min_bpm = None
        max_bpm = None

        for bpm_change in value.split(","):
          bpm = float(bpm_change.split("=")[1])

          if min_bpm is None or bpm < min_bpm:
            min_bpm = bpm

          if max_bpm is None or bpm > max_bpm:
            max_bpm = bpm

        self.song.bpm_range = (min_bpm, max_bpm)

        if min_bpm == max_bpm:
          self.song.bpm_type = BPM.FIXED
        else:
          self.song.bpm_type = BPM.VARIES
    elif name == "DISPLAYBPM":
      if value == "*":
        self.song.bpm_type = BPM.RANDOM
      else:
        bpm = value.split(":")

        if len(bpm) == 1:
          bpm = float(bpm[0])
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

    chart.type = ChartInfo.Type.convert(note_data[0])
    chart.difficulty = ChartInfo.Difficulty.convert(note_data[2])
    chart.meter = int(note_data[3])

    # TODO: Handle other chart types
    if chart.type == ChartInfo.Type.DANCE_SINGLE:
      self.parse_notes(chart, note_data[5])
    else:
      print("Unsupported chart type '%s' (%s), skipping..." % (note_data[0], chart.type))
      return

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
        for note in row:
          try:
            note_type = StepInfo.Type(note)
          except ValueError:
            continue

          if note_type == StepInfo.Type.EMPTY:
            continue

          # Handle notes for each key
          if note_type == StepInfo.Type.MINE:
            chart.steps.mines += 1
          elif note_type == StepInfo.Type.LIFT:
            chart.steps.lifts += 1
          elif note_type == StepInfo.Type.FAKE:
            chart.steps.fakes += 1
          elif note_type == StepInfo.Type.TAP:
            consecutive_taps += 1
          elif note_type == StepInfo.Type.HOLD:
            consecutive_taps += 1
            chart.steps.holds += 1
          elif note_type == StepInfo.Type.ROLL:
            consecutive_taps += 1
            chart.steps.rolls += 1

        # Handle how many directions have to be pressed at once
        if consecutive_taps == 2:
          chart.steps.jumps += 1
        elif consecutive_taps >= 3:
          chart.steps.jumps += 1
          chart.steps.hands += 1

        # There seems to be an inconsistency with how the stepmania note editor and the song
        # browser classifies taps. The editor counts every note as a tap whereas the browser
        # considers jumps and hands to only be a single tap. This doesn't affect anything
        # but it can make testing confusing if you are using the editor as a reference
        chart.steps.taps += min(1, consecutive_taps)
        row = ""
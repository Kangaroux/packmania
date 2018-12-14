from enum import Enum


class BPM(Enum):
  FIXED = "fixed"
  RANDOM = "random"
  VARIES = "varies"


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
    self.fakes = 0
    self.hands = 0
    self.holds = 0
    self.jumps = 0
    self.lifts = 0
    self.mines = 0
    self.rolls = 0
    self.taps = 0


class ChartInfo:
  """ Information for each difficulty """

  class Type(Enum):
    DANCE_SINGLE = "dance-single"
    DANCE_DOUBLE = "dance-double"
    # DANCE_SOLO = "dance-solo"
    # DANCE_THREEPANEL = "dance-threepanel"
    # DANCE_ROUTINE = "dance-routine"

    @classmethod
    def convert(cls, name):
      name = name.lower()
      type_map = {
        "dance-single": cls.DANCE_SINGLE,
        "dance-solo": cls.DANCE_SINGLE,
        "dance-double": cls.DANCE_DOUBLE,
        "dance-couple": cls.DANCE_DOUBLE
      }

      return type_map.get(name)

  class Difficulty(Enum):
    NOVICE = "Novice"
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"
    EXPERT = "Expert"
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
    self.type = None
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
    self.has_stops = False
    self.bpm_type = BPM.FIXED

    # When set, this is a 2-tuple of the min and max values for the BPM. If the BPM
    # does not change the min and max will be equal
    self.bpm_range = None
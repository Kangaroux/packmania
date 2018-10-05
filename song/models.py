from django.db import models

from lib.parser.sm import BPM, ChartInfo


CHART_CHOICES = (
  (ChartInfo.Type.DANCE_SINGLE.value, "Dance single"),
  (ChartInfo.Type.DANCE_DOUBLE.value, "Dance double"),
)

DIFFICULTY_CHOICES = (
  (ChartInfo.Difficulty.NOVICE.value, "Novice"),
  (ChartInfo.Difficulty.EASY.value, "Easy"),
  (ChartInfo.Difficulty.MEDIUM.value, "Medium"),
  (ChartInfo.Difficulty.HARD.value, "Hard"),
  (ChartInfo.Difficulty.EXPERT.value, "Expert"),
  (ChartInfo.Difficulty.EDIT.value, "Edit"),
)

GENRE_CHOICES = (
  ("anime", "Anime"),
  ("chiptune", "Chiptune"),
  ("dnb", "Drum and Bass"),
  ("electronic", "Electronic"),
  ("happy_hardcore", "Happy Hardcore"),
  ("hardcore", "Hardcore (Gabber)"),
  ("pop", "Pop"),
  ("hiphop", "Rap/Hip Hop"),
  ("rock", "Rock/Metal"),
  ("videogame", "Video Game"),

  ("other", "Other"),

  # This must be the last genre
  ("unknown", "Not Specified")
)

BPM_CHOICES = (
  (BPM.FIXED.value, "Fixed"),
  (BPM.RANDOM.value, "Random"),
  (BPM.VARIES.value, "Varies")
)


class Chart(models.Model):
  # Metadata for the chart
  type = models.CharField(max_length=50, choices=CHART_CHOICES)
  meter = models.IntegerField(default=1)
  difficulty = models.CharField(max_length=50, choices=DIFFICULTY_CHOICES)

  # Note counts
  fakes = models.IntegerField(default=0)
  hands = models.IntegerField(default=0)
  holds = models.IntegerField(default=0)
  jumps = models.IntegerField(default=0)
  lifts = models.IntegerField(default=0)
  mines = models.IntegerField(default=0)
  rolls = models.IntegerField(default=0)
  taps = models.IntegerField(default=0)

  song = models.ForeignKey("Song", related_name="charts", on_delete=models.CASCADE)


class Song(models.Model):
  uploader = models.ForeignKey("user.User", on_delete=models.CASCADE)

  artist = models.CharField(max_length=100)

  # TODO: Allow author to be a string or a foreign key to a user
  author = models.CharField(max_length=100)
  genre = models.CharField(max_length=50, choices=GENRE_CHOICES, default=GENRE_CHOICES[-1])
  subtitle = models.CharField(max_length=100)
  title = models.CharField(max_length=100)

  has_stops = models.BooleanField(default=False)
  bpm_type = models.CharField(max_length=50, choices=BPM_CHOICES)
  min_bpm = models.FloatField(default=60.0)
  max_bpm = models.FloatField(default=60.0)

  banner_url = models.CharField(max_length=255, null=True)
  download_url = models.CharField(max_length=255)

  # .mp3 for the song preview
  preview_url = models.CharField(max_length=255)
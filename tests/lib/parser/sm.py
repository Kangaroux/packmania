import os.path

from django.conf import settings
from django.test import TestCase

from lib.sm_parser import BPM, ChartInfo, SMParser


ABXY_FILE = os.path.join(settings.TEST_DATA_DIR, "ABXY", "abxy.sm")


class TestSMParser(TestCase):
  def setUp(self):
    self.p = SMParser()


  def test_parse_display_info(self):
    self.p.load_file(ABXY_FILE)
    data = self.p.display

    self.assertEqual(data.artist, "Popskyy")
    self.assertEqual(data.author, "")
    self.assertEqual(data.background, "abxy-bg.png")
    self.assertEqual(data.banner, "abxy-banner.png")
    self.assertEqual(data.genre, "Chiptune")
    self.assertEqual(data.subtitle, "")
    self.assertEqual(data.title, "ABXY")

  def test_parse_song_info(self):
    self.p.load_file(ABXY_FILE)
    data = self.p.song

    self.assertEqual(data.file_name, "abxy.ogg")
    self.assertEqual(data.preview_start, 32.808270)
    self.assertEqual(data.preview_length, 14.545456)
    self.assertEqual(data.bpm_type, BPM.FIXED)
    self.assertEqual(data.bpm_range, (132.0, 132.0))
    self.assertEqual(data.has_stops, False)

  def test_abxy_parse_chart_metadata(self):
    self.p.load_file(ABXY_FILE)
    charts = sorted(self.p.charts, key=lambda chart: chart.meter)

    self.assertEqual(len(charts), 4)

    # Easy single
    self.assertEqual(charts[0].type, ChartInfo.Type.DANCE_SINGLE)
    self.assertEqual(charts[0].meter, 3)
    self.assertEqual(charts[0].difficulty, ChartInfo.Difficulty.EASY)
    self.assertEqual(charts[0].steps.taps, 157)
    self.assertEqual(charts[0].steps.jumps, 2)
    self.assertEqual(charts[0].steps.holds, 13)
    self.assertEqual(charts[0].steps.mines, 0)
    self.assertEqual(charts[0].steps.hands, 0)
    self.assertEqual(charts[0].steps.rolls, 0)
    self.assertEqual(charts[0].steps.lifts, 0)
    self.assertEqual(charts[0].steps.fakes, 0)

    # Medium single
    self.assertEqual(charts[1].type, ChartInfo.Type.DANCE_SINGLE)
    self.assertEqual(charts[1].meter, 5)
    self.assertEqual(charts[1].difficulty, ChartInfo.Difficulty.MEDIUM)
    self.assertEqual(charts[1].steps.taps, 222)
    self.assertEqual(charts[1].steps.jumps, 35)
    self.assertEqual(charts[1].steps.holds, 20)
    self.assertEqual(charts[1].steps.rolls, 7)

    # Hard single
    self.assertEqual(charts[2].type, ChartInfo.Type.DANCE_SINGLE)
    self.assertEqual(charts[2].meter, 9)
    self.assertEqual(charts[2].difficulty, ChartInfo.Difficulty.HARD)
    self.assertEqual(charts[2].steps.taps, 410)
    self.assertEqual(charts[2].steps.jumps, 43)
    self.assertEqual(charts[2].steps.holds, 39)
    self.assertEqual(charts[2].steps.rolls, 8)

    # Expert single
    self.assertEqual(charts[3].type, ChartInfo.Type.DANCE_SINGLE)
    self.assertEqual(charts[3].meter, 11)
    self.assertEqual(charts[3].difficulty, ChartInfo.Difficulty.EXPERT)
    self.assertEqual(charts[3].steps.taps, 551)
    self.assertEqual(charts[3].steps.jumps, 47)
    self.assertEqual(charts[3].steps.holds, 56)
    self.assertEqual(charts[3].steps.rolls, 0)
from unittest import TestCase

from lib import util


class TestUtilFunctions(TestCase):
  def test_first(self):
    lst = ["apple", "banana", "cherry"]

    self.assertEqual(util.first(lst, lambda x: x == "apple"), ("apple", 0))
    self.assertEqual(util.first(lst, lambda x: x == "banana"), ("banana", 1))
    self.assertEqual(util.first(lst, lambda x: x == "cherry"), ("cherry", 2))
    self.assertEqual(util.first(lst, lambda x: x == "tomato"), (None, -1))
    self.assertEqual(util.first([], lambda x: x is not None), (None, -1))

  def test_rename(self):
    self.assertEqual(util.rename_file("test", "new"), "new")
    self.assertEqual(util.rename_file("test.png", "image"), "image.png")
    self.assertEqual(util.rename_file("a.b.c", "foo"), "foo.b.c")
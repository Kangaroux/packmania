import os.path
import random
import uuid


def first(iterable, func):
  """ Checks every element with `func` until `func` returns truthy. Returns a
  2-tuple of the matching element and its index. If no element is found, returns
  (None, -1)
  """
  for i in range(len(iterable)):
    if func(iterable[i]):
      return (iterable[i], i)

  return (None, -1)


def rename_file(file, new_name):
  """ Returns the new name for a file while keeping all of extensions intact.

  rename("foo.png", "bar") => "bar.png"
  """
  parts = file.split(".", 1)

  # File name has an extension
  if len(parts) == 2:
    new_name = "%s.%s" % (new_name, parts[1])

  return new_name


hex_chars = "0123456789abcdef"

def random_hex_string(length):
  """ Returns a pseudo-random hex string of a given length. The first 32 bytes
  are gauranteed to be unique
  """
  s = uuid.uuid4().hex[:length]

  for _ in range(length - 32):
    s += random.choice(hex_chars)

  return s
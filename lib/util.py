import os.path


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
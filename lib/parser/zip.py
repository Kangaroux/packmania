from zipfile import ZipFile, ZipInfo


def zip_as_tree(zip_file):
  """ Returns a dictionary tree of the files and directories in the zip """
  tree = {}

  for file in zip_file.infolist():
    path = file.filename.split("/")
    cursor = tree

    for p in path[:-1]:
      cursor.setdefault(p, {})
      cursor = cursor[p]

    if not file.is_dir(): # type: ignore
      cursor[path[-1]] = file

  return tree


def get_uncompressed_size(tree):
  """ Recursively finds the total size of the zip file after it has
  been uncompressed
  """
  size = 0

  for k in tree:
    v = tree[k]

    if isinstance(v, dict):
      size += get_uncompressed_size(v)
    else:
      size += v.file_size

  return size


def contains_file_ext(tree, ext):
  """ Returns True if the zip contains a file with one of the given extensions """
  for k in tree:
    v = tree[k]

    if isinstance(v, dict) and contains_file_ext(v, ext):
      return True
    elif any([ k.endswith(e) for e in ext ]):
      return True

  return False


def get_single_song(tree):
  """ Looks for a .sm file in `tree`. It's an error if `tree` doesn't contain
  exactly one .sm file or if it contains a folder
  """
  sm_file = None

  for k in tree:
    v = tree[k]

    if isinstance(v, dict):
      raise Exception("Songs cannot contain a subfolder")
    elif k.endswith(".sm"):
      if sm_file:
        raise Exception("Songs must only have one .sm file")

      sm_file = v

  if not sm_file:
    raise Exception("Songs must have a .sm file")

  return sm_file

def get_songs(tree):
  """ Inspects the zip to validate the folder structure and returns whether the
  zip is a pack or not as well as a list of the .sm files in the pack.

  Valid folder structures:

  - Song files without a root folder
  - Song files with a root folder
  - (Pack) Multiple song folders and optionally extra files at the root
  - (Pack) Like the previous but contained in a root folder (which we can infer
           the pack's name from)
  """
  is_pack = False
  pack_name = None
  sm_files = []

  root_folders = {}
  num_root_files = 0

  # Start by counting the number of folders at the root level
  for k in tree:
    if isinstance(tree[k], dict):
      root_folders[k] = tree[k]
    else:
      num_root_files += 1

  # Looks like a song with no root folders
  if len(root_folders) == 0:
    sm_files.append(get_single_song(tree))
  elif len(root_folders) == 1:
    folder = list(root_folders.values())[0]

    # Possibly a pack with one song but most likely an error
    if num_root_files > 0:
      try:
        sm_files.append(get_single_song(folder))
      except:
        raise Exception("Unexpected files found at root of zip")
    else:
      is_pack = True
      pack_name = list(root_folders.keys())[0]

      for f in folder:
        # Packs can contain files such as images or READMEs
        if isinstance(folder[f], dict):
          sm_files.append(get_single_song(folder[f]))
  else:
    is_pack = True

    # Multiple folders means this should be a pack
    for f in root_folders:
      sm_files.append(get_single_song(root_folders[f]))

  return ( is_pack, pack_name, sm_files )

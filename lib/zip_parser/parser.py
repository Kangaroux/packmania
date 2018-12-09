from zipfile import ZipFile, ZipInfo

from .exceptions import *


class ZipParser:
  """ A parser for opening zips containing a song(s)/pack.  """

  def __init__(self, file):
    # A file-like object
    self.file = file
    self.zf = None

    # A dictionary of the folder/file structure
    self.tree = None

    self.is_pack = False
    self.pack_name = None
    self.step_files = None
    self.disallowed_files = None
    self.uncompressed_size = None

  def __enter__(self):
    self.zf = zip_file.ZipFile(self.file)

  def __exit__(self):
    self.zf.close()
    self.zf = None

  def inspect(self, max_size=None, disallowed_files=None):
    """ Inspects the zip file and raises an exception if it failed the inspection """
    self.tree = self._build_tree()
    self.uncompressed_size = self._get_uncompressed_size(self.tree)

    if max_size and self.uncompressed_size < max_size:
      raise ZipTooLargeError

    self.disallowed_files = self._get_files_with_ext(self.tree, disallowed_files)

    if self.disallowed_files:
      raise ZipBadFilesError

    self.is_pack, self.pack_name, self.step_files = self._find_all_step_files(self.tree)

  def _build_tree(self):
    """ Iterates over the file paths in the zip and converts them into a dictionary tree
    to make lookups easier later on
    """
    tree = {}

    for file in self.zf.infolist():
      path = file.filename.split("/")
      cursor = tree

      # Create folders for each directory in the path and move the cursor into the dir
      for p in path[:-1]:
        cursor.setdefault(p, {})
        cursor = cursor[p]

      # Add the file to the tree if it's actually a file
      if not file.is_dir():
        cursor[path[-1]] = file

    return tree

  def _get_uncompressed_size(self, tree):
    """ Recursively finds the total size of the zip file after it has been uncompressed """
    size = 0

    for k in tree:
      v = tree[k]

      if isinstance(v, dict):
        size += get_uncompressed_size(v)
      else:
        size += v.file_size

    return size

  def _get_files_with_ext(self, tree, ext, files=None):
    """ Returns a list of files that have any of the given extensions """
    if ext is None:
      return []
    elif files is None:
      files = []

    for k in tree:
      v = tree[k]

      if isinstance(v, dict)
        self._get_files_with_ext(v, ext, files)

      for e in ext:
        if v.endswith(e):
          files.append(v)
          break

    return files

  def _find_step_file(self, subtree):
    """ Searches for a single .sm file in the subtree and returns it, else raises an error
    if there are none or multiple .sm files
    """
    sm_file = None

    for k in subtree:
      v = subtree[k]

      if isinstance(v, dict):
        raise ZipSubfolderError
      elif k.endswith(".sm"):
        if sm_file:
          raise ZipMultipleStepFilesError

        sm_file = v

    if not sm_file:
      raise ZipMissingStepFileError

    return sm_file

  def _find_all_step_files(self, tree):
    """ Finds all of the step files in the zip while also verifying that the folder
    structure is valid.

    Valid folder structures:

    - Song files without a root folder
    - Song files with a root folder
    - (Pack) Multiple song folders and optionally extra files at the root
    - (Pack) Like the previous but contained in a root folder (which we can infer
            the pack's name from)
    """
    is_pack = False
    pack_name = None
    step_files = []

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
      if num_root_files == 0:
        raise ZipEmptyError

      step_files.append(get_single_song(tree))
    elif len(root_folders) == 1:
      folder = list(root_folders.values())[0]

      # Possibly a pack with one song but most likely an error
      if num_root_files > 0:
        try:
          step_files.append(get_single_song(folder))
        except:
          raise ZipUnexpectedRootFilesError
      else:
        # Check if there are more folders inside. If not then this is a zip with
        # a single song contained within a root folder
        for f in folder:
          if isinstance(folder[f], dict):
            is_pack = True
            pack_name = list(root_folders.keys())[0]
            break

        if is_pack:
          for f in folder:
            # Packs can contain files such as images or READMEs
            if isinstance(folder[f], dict):
              step_files.append(get_single_song(folder[f]))
        else:
          step_files.append(get_single_song(folder))
    else:
      is_pack = True

      # Multiple folders means this should be a pack
      for f in root_folders:
        step_files.append(get_single_song(root_folders[f]))

    return ( is_pack, pack_name, step_files )

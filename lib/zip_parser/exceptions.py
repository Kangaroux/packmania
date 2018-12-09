class BaseZipError(Exception):
  pass


class BadZipError(BaseZipError):
  """ This is the same as zipfile.BadZipFile """


class ZipTooLargeError(BaseZipError):
  """ The uncompressed size of the zip file is too large """
  pass


class BadFilesError(BaseZipError):
  """ The zip contains disallowed file extensions """
  pass


class SubfolderError(BaseZipError):
  """ A subfolder was found in a song folder """
  pass


class MultipleStepFilesError(BaseZipError):
  """ Multiple step files of the same type were found in a song folder """
  pass


class MissingStepFileError(BaseZipError):
  """ No step file was found in a song folder """
  pass


class ZipEmptyError(BaseZipError):
  """ The zip is completely empty """
  pass


class UnexpectedRootFilesError(BaseZipError):
  """ The zip has unexpected files at the root level """
  pass
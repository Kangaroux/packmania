class BaseZipError(Exception):
  pass


class ZipTooLargeError(BaseZipError):
  """ The uncompressed size of the zip file is too large """
  pass


class ZipBadFilesError(BaseZipError):
  """ The zip contains disallowed file extensions """
  pass


class ZipSubfolderError(BaseZipError):
  """ A subfolder was found in a song folder """
  pass


class ZipMultipleStepFilesError(BaseZipError):
  """ Multiple step files of the same type were found in a song folder """
  pass


class ZipMissingStepFileError(BaseZipError):
  """ No step file was found in a song folder """
  pass


class ZipEmptyError(BaseZipError):
  """ The zip is completely empty """
  pass


class ZipUnexpectedRootFilesError(BaseZipError):
  """ The zip has unexpected files at the root level """
  pass
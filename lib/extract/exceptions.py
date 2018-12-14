class ExtractError(Exception):
  pass


class MissingAudioFileError(ExtractError):
  """ The audio file is missing """
  pass


class StepFileParseError(ExtractError):
  """ An exception occurred while trying to parse the step file """
  pass
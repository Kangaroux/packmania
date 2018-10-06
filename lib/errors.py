# New min/max length error messages
def error_messages(extra=None):
  return {
    "error_messages": {
      "max_length": "Cannot be longer than %(limit_value)d characters.",
      "min_length": "Must be at least %(limit_value)d characters.",
      "blank": "This field is required.",
      **(extra or {})
    }
  }
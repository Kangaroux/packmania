import os
from .settings import *


DEBUG = False
DEV = False
SECRET_KEY = os.environ.get("SECRET_KEY")

REST_FRAMEWORK = {
  "DEFAULT_RENDERER_CLASSES": (
    "rest_framework.renderers.JSONRenderer",
  )
}
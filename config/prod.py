from .settings import *

DEBUG = False
DEV = False

REST_FRAMEWORK = {
  "DEFAULT_RENDERER_CLASSES": (
    "rest_framework.renderers.JSONRenderer",
  )
}
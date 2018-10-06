import logging
from django.http import JsonResponse

from rest_framework.views import APIView as RestFrameworkAPIView


logger = logging.getLogger(__name__)


class APIError(Exception):
  def __init__(self, msg, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.msg = msg

  def as_json(self):
    return APIView.error(self.msg, status=404)


class MissingError(APIError):
  pass


class LoginRequiredMixin:
  """ View mixin which returns a 401 if the user is not logged in. By default the
  mixin only protects the POST, PATCH, and DELETE methods
  """

  PROTECTED_METHODS = ["POST", "PATCH", "DELETE"]

  def dispatch(self, request, *args, **kwargs):
    if not request.user.is_authenticated and request.method.upper() in self.PROTECTED_METHODS:
      return APIView.not_logged_in()
    else:
      return super().dispatch(request, *args, **kwargs)


class APIView(RestFrameworkAPIView):
  """ Base API view which includes some common methods for returning responses
  and checking authorization
  """

  def dispatch(self, *args, **kwargs):
    try:
      return super().dispatch(*args, **kwargs)
    except APIError as e:
      return e.as_json()
    except Exception as e:
      logger.exception("Unexpected exception occurred in API view")
      return self.error("An unexpected error occurred.", status=500)

  @classmethod
  def form_error(cls, form, msg=None):
    return cls.field_errors(form.errors, msg)

  @classmethod
  def serializer_error(cls, errors, msg=None):
    return cls.field_errors(errors, msg)

  @classmethod
  def field_errors(cls, errors, msg=None):
    # Any generic form-wide error(s) are included under the __all__ key
    form_error_msg = errors.pop("__all__", None)

    if not msg:
      if form_error_msg:
        msg = form_error_msg[0]
      else:
        msg = "Some fields are missing or incorrect."

    return cls.error(msg, {
      "fields": { k:v[0] for k, v in errors.items() }
    })

  @staticmethod
  def error(msg, data=None, status=400):
    resp = {
      "status": "error",
      "msg": msg
    }

    if data:
      resp.update(data)

    return JsonResponse(resp, status=status)

  @staticmethod
  def ok(data=None, msg=None, status=200):
    resp = {
      "status": "ok"
    }

    if msg:
      resp["msg"] = msg

    if data is not None:
      if isinstance(data, list):
        resp["results"] = data
      else:
        resp.update(data)

    return JsonResponse(resp, status=status)

  @classmethod
  def not_logged_in(cls):
    return cls.error("You must be logged in to do that.", status=401)

  @classmethod
  def lacks_permission(cls):
    return cls.error("You do not have permission to do that.", status=403)
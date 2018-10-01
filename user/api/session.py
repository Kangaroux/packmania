from django.contrib.auth import login, logout

from ..forms import LoginForm
from ..models import User
from lib.api import APIView


class SessionAPI(APIView):
  """ Session API for logging in, logging out, and checking if a user is authenticated """

  def get(self, request, format=None):
    """ Returns the user id of the current user if they are logged in (or None) """
    return self.ok({
      "authenticated": request.user.is_authenticated,
      "user_id": request.user.id
    })

  def post(self, request, format=None):
    """ Logs the user in and returns their user id """
    form = LoginForm(request.data)

    if not form.is_valid():
      return self.form_error(form)

    login(request, form.user)

    return self.ok({ "user_id": request.user.id })

  def delete(self, request, format=None):
    """ Logs the user out and clears their session """
    logout(request)
    return self.ok()
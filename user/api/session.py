from django.contrib.auth import login, logout

from ..forms import LoginForm
from ..models import User
from ..serializers import UserSerializer
from lib.api import APIView


class SessionAPI(APIView):
  """ Session API for logging in, logging out, and checking if a user is authenticated """

  def get(self, request, format=None):
    """ Returns the current user if they are logged in """
    data = {
      "authenticated": request.user.is_authenticated
    }

    if request.user.is_authenticated:
      data["user"] = UserSerializer(request.user, show_private_fields=True).data
    else:
      data["user"] = None

    return self.ok(data)

  def post(self, request, format=None):
    """ Tries to log the user in. If the login was successful returns the same response
    as calling `get`
    """
    form = LoginForm(request.data)

    if not form.is_valid():
      return self.form_error(form)

    login(request, form.user)

    # Expire the user's session when they close their browser
    if not form.cleaned_data.get("remember_me"):
      request.session.set_expiry(0)

    return self.get(request)

  def delete(self, request, format=None):
    """ Logs the user out and clears their session """
    logout(request)
    return self.ok()
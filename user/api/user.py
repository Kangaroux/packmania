from django.contrib.auth import update_session_auth_hash

from ..models import User
from ..serializers import PRIVATE_FIELDS, UserSerializer
from lib.api import APIView, LoginRequiredMixin


class UserListAPI(APIView):
  """ User API for getting collections of users or creating a new user """

  def get(self, request, format=None):
    """ Get multiple users """

    # TODO: Filtering, pagination
    return self.ok(UserSerializer(User.objects.all(), many=True).data)

  def post(self, request, format=None):
    """ Create a new user """
    if request.user.is_authenticated:
      return self.error("Logout before trying to create a new user.")

    serializer = UserSerializer(data=request.data)

    if not serializer.is_valid():
      return self.serializer_error(serializer.errors)

    u = serializer.create(serializer.validated_data)

    return self.ok({ "user": UserSerializer(u).data }, status=201)


class UserDetailAPI(LoginRequiredMixin, APIView):
  """ User API for getting, updating, and deleting an existing user """

  def get(self, request, pk, format=None):
    """ Get a single user """
    try:
      data = { "user": UserSerializer(User.objects.get(pk=pk), show_private_fields=request.user.id == pk).data }
    except User.DoesNotExist:
      return self.error("User does not exist.", status=404)

    return self.ok(data)

  def patch(self, request, pk, format=None):
    """ Update a user """

    # Verify the user has permission to do this
    if request.user.id != pk:
      return self.lacks_permission()

    try:
      u = User.objects.get(pk=pk)
    except User.DoesNotExist:
      return self.error("User does not exist.", status=404)

    serializer = UserSerializer(u, data=request.data, partial=True)

    if not serializer.is_valid():
      return self.serializer_error(serializer.errors)

    serializer.update(u, serializer.validated_data)

    # Don't invalidate the user's session if they were the one who made this request
    if request.user == u:
      update_session_auth_hash(request, u)

    return self.ok({ "user": UserSerializer(u).data })

  def delete(self, request, pk, format=None):
    """ Delete a user """

    # Verify the user has permission to do this
    if request.user.id != pk:
      return self.lacks_permission()

    try:
      u = User.objects.get(pk=pk)
    except User.DoesNotExist:
      return self.error("User does not exist.", status=404)

    u.is_active = False
    u.save()

    return self.ok()
from django.contrib.auth import update_session_auth_hash
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer
from lib.api import APIView


class UserList(APIView):
  def get(self, request, format=None):
    """ Get multiple users """
    return self.ok(UserSerializer(User.objects.all(), many=True).data)

  def post(self, request, format=None):
    """ Create a new user """
    serializer = UserSerializer(data=request.data)

    if not serializer.is_valid():
      return self.serializer_error(serializer.errors)

    u = serializer.create(serializer.validated_data)

    return self.ok({ "user": UserSerializer(u).data }, status=201)

class UserDetail(APIView):
  def get(self, request, pk, format=None):
    """ Get a single user """
    try:
      return self.ok({ "user": UserSerializer(User.objects.get(pk=pk)).data })
    except User.DoesNotExist:
      return self.error("User does not exist.", status=404)

  def patch(self, request, pk, format=None):
    """ Update a user """
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
    try:
      u = User.objects.get(pk=pk)
    except User.DoesNotExist:
      return self.error("User does not exist.", status=404)

    u.is_active = False
    u.save()

    return self.ok()
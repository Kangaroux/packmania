from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UserSerializer


class UserList(APIView):
  def get(self, request, format=None):
    """ Get multiple users """
    return Response(UserSerializer(User.objects.all(), many=True).data)

  def post(self, request, format=None):
    """ Create a new user """
    serializer = UserSerializer(data=request.data)

    if not serializer.is_valid():
      return JsonResponse(serializer.errors, status=400)

    u = serializer.create(serializer.validated_data)

    return JsonResponse(UserSerializer(u).data)

class UserDetail(APIView):
  def get(self, request, pk, format=None):
    """ Get a single user """
    try:
      return JsonResponse(UserSerializer(User.objects.get(pk=pk)).data)
    except User.DoesNotExist:
      return JsonResponse({ "error": "User does not exist." }, status=404)

  def patch(self, request, pk, format=None):
    """ Update a user """
    try:
      u = User.objects.get(pk=pk)
    except User.DoesNotExist:
      return JsonResponse({ "error": "User does not exist." }, status=404)

    serializer = UserSerializer(u, data=request.data, partial=True)

    if not serializer.is_valid():
      return JsonResponse(serializer.errors, status=400)

    serializer.update(u, serializer.validated_data)

    # Don't invalidate the user's session if they were the one who made this request
    if request.user.id == u.id:
      update_session_auth_hash(request, u)

    return JsonResponse(UserSerializer(u).data)
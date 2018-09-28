from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import CreateUserSerializer, DetailUserSerializer


class UserList(APIView):
  def get(self, request, format=None):
    return Response(DetailUserSerializer(User.objects.all(), many=True).data)

  def post(self, request, format=None):
    serializer = CreateUserSerializer(data=request.data)

    if not serializer.is_valid():
      return JsonResponse(serializer.errors, status=400)

    u = User(**serializer.validated_data)
    u.set_password(serializer.data.get("password"))
    u.save()

    return JsonResponse(DetailUserSerializer(u).data)

class UserDetail(APIView):
  def get(self, request, pk, format=None):
    try:
      return JsonResponse(DetailUserSerializer(User.objects.get(pk=pk)).data)
    except User.DoesNotExist:
      return JsonResponse({ "error": "User does not exist." })
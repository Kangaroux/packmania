from rest_framework import serializers
from rest_framework.fields import CharField
from rest_framework.serializers import ValidationError

from lib.errors import error_messages
from .models import Chart, Song


class ChartSerializer(serializers.ModelSerializer):
  class Meta:
    model = Chart
    fields = "__all__"


class SongSerializer(serializers.ModelSerializer):
  class Meta:
    model = Song
    fields = "__all__"

  charts = ChartSerializer(many=True, read_only=True)

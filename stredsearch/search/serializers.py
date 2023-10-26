from rest_framework import serializers

from .models import *


class StackUserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    gibberish = serializers.CharField(max_length=500, required=False)

    class Meta:
        model = StackUser

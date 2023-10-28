from rest_framework import serializers

from .models import *


class StackUserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=False)
    display_name = serializers.CharField(max_length=200)
    gibberish = serializers.CharField(max_length=500, required=False)

    class Meta:
        model = StackUser

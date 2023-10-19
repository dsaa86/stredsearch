from rest_framework import serializers
from .models import *

class StackQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StackQuestion
        fields = '__all__'

class StackUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = StackUser
        fields = '__all__'

class StackRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = StackRoute
        fields = '__all__'

class StackMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = StackMeta
        fields = '__all__'
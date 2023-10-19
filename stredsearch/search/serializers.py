from rest_framework import serializers
from .models import *

class StackQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StackQuestion
        fields = '__all__'
    # created_on_stredsearch = serializers.DateTimeField(read_only=True)
    # updated_on_stredsearch = serializers.DateTimeField(read_only=True)
    # is_answered = serializers.BooleanField(read_only=True)
    # view_count = serializers.IntegerField(read_only=True)
    # answer_count = serializers.IntegerField(read_only=True)
    # score = serializers.IntegerField(read_only=True)
    # last_activity_date = serializers.DateTimeField(read_only=True)
    # creation_date = serializers.DateTimeField(read_only=True)
    # last_edit_date = serializers.DateTimeField(read_only=True)
    # question_id = serializers.IntegerField(read_only=True)
    # link = serializers.CharField(read_only=True)
    # title = serializers.CharField(read_only=True)

class StackUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = StackUser
        fields = '__all__'
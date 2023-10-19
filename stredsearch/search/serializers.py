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

class RedditSearchQuerySerializer(serializers.Serializer):
    title = serializers.CharField(max_length = 500)
    link = serializers.CharField(max_length = 500)

class StackSearchQuerySerializer(serializers.Serializer):
    is_answered = serializers.BooleanField()
    view_count = serializers.IntegerField()
    answer_count = serializers.IntegerField()
    last_activity_date = serializers.DateTimeField()
    creation_date = serializers.DateTimeField()
    last_edit_date = serializers.DateTimeField()
    question_id = serializers.IntegerField()
    link = serializers.CharField(max_length = 500)
    title = serializers.CharField(max_length = 500)
    user_id = serializers.IntegerField()
    display_name = serializers.CharField(max_length = 500)
from rest_framework import serializers
from search.models import *


class StackTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StackTags
        fields = "__all__"

class StackParamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StackParams
        fields = "__all__"

class StackFiltersSerializer(serializers.ModelSerializer):
    class Meta:
        model = StackFilters
        fields = "__all__"

class StackSortMethodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StackSortMethods
        fields = "__all__"


class StackOrderMethodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StackOrderMethods
        fields = "__all__"

class StackQuestionDataFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StackQuestionDataFields
        fields = "__all__"



class StackQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StackQuestion
        fields = "__all__"


class StackUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = StackUser
        fields = "__all__"


class StackRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = StackRoute
        fields = "__all__"


class StackMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = StackRouteMeta
        fields = "__all__"


class RedditSearchQuerySerializer(serializers.Serializer):
    title = serializers.CharField(max_length=500)
    link = serializers.CharField(max_length=500)


class StackSearchQuerySerializer(serializers.Serializer):
    tags = serializers.CharField()
    is_answered = serializers.BooleanField()
    view_count = serializers.IntegerField()
    answer_count = serializers.IntegerField()
    score = serializers.IntegerField()
    # There may never have been activity on the question
    last_activity_date = serializers.DateTimeField(required=False)
    creation_date = serializers.DateTimeField()
    # The question may never have been edited
    last_edit_date = serializers.DateTimeField(required=False)
    question_id = serializers.IntegerField()
    link = serializers.CharField(max_length=500)
    title = serializers.CharField(max_length=500)
    # user may have deleted account, questions with this occurence do not return a user_id and will throw an error if the field presence is enforeced
    user_id = serializers.IntegerField(required=False)
    display_name = serializers.CharField(max_length=500)


class StackSearchErrorSerializer(serializers.Serializer):
    error = serializers.CharField(max_length=500)


class StackCategoriesSerializer(serializers.Serializer):
    category = serializers.CharField(max_length=50)


class StackRoutesSerializer(serializers.Serializer):
    route = serializers.CharField(max_length=50)


class StackRoutesURLAndParamsSerializer(serializers.Serializer):
    url = serializers.CharField(max_length=100)
    params = serializers.CharField(max_length=250)

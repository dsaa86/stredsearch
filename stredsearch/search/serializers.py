from dataclasses import fields

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator
from search.models import *


class RedditSearchTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RedditSearchType
        fields = "__all__"


class RedditSubredditSerializer(serializers.ModelSerializer):
    class Meta:
        model = RedditSubreddit
        fields = "__all__"


class RedditQuestionSerializer(serializers.ModelSerializer):
    search_type = RedditSearchTypeSerializer(read_only=True, many=True)
    subreddit = RedditSubredditSerializer(read_only=True, many=True)

    class Meta:
        model = RedditQuestion
        fields = "__all__"


class StackOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StackUser
        fields = "__all__"


class StackOwnerSerializerLocalSearch(serializers.ModelSerializer):
    class Meta:
        model = StackUser
        fields = ["user_id", "display_name"]

    def to_representation(self, instance):
        return (instance.user_id, instance.display_name)


class StackQuestionTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = StackTags
        fields = "__all__"


class StackQuestionTagSerializerLocalSearch(serializers.ModelSerializer):
    class Meta:
        model = StackTags
        fields = ["id", "tag_name"]

    def to_representation(self, instance):
        return instance.tag_name


class StackQuestionSerializer(serializers.ModelSerializer):
    owner = StackOwnerSerializer(read_only=True)
    tags = StackQuestionTagSerializer(read_only=True, many=True)

    class Meta:
        model = StackQuestion
        fields = "__all__"


class SearchTermsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchTerms
        fields = ["search_term"]


class RetrieveSearchResultsSerializer(serializers.ModelSerializer):
    search_term = SearchTermsSerializer(read_only=True)
    stack_responses = StackQuestionSerializer(read_only=True, many=True)
    reddit_responses = RedditQuestionSerializer(read_only=True, many=True)

    class Meta:
        model = UserSearchResponses
        fields = "__all__"


class UserSearchResponsesSerializer(serializers.ModelSerializer):
    search_term = SearchTermsSerializer(read_only=True)

    class Meta:
        model = UserSearchResponses
        fields = ["search_term", "search_term"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "password2")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"], email=validated_data["email"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


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
    question_title = serializers.CharField(max_length=500)
    question_link = serializers.CharField(max_length=500)


class RedditSearchQuerySerializerForFiltering(serializers.Serializer):
    link = serializers.CharField(max_length=500)
    title = serializers.CharField(max_length=500)
    subreddit = serializers.CharField(max_length=500)


class StackSearchQuerySerializer(serializers.ModelSerializer):
    tags = StackQuestionTagSerializerLocalSearch(read_only=True, many=True)
    owner = StackOwnerSerializerLocalSearch(read_only=True)

    class Meta:
        model = StackQuestion
        fields = "__all__"


class RedditSearchQuerySerializer(serializers.ModelSerializer):
    subreddit = RedditSubredditSerializer(read_only=True, many=True)

    class Meta:
        model = RedditQuestion
        fields = "__all__"


class StackSearchErrorSerializer(serializers.Serializer):
    error = serializers.CharField(max_length=500)


class StackCategoriesSerializer(serializers.Serializer):
    category = serializers.CharField(max_length=50)


class StackRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = StackRoute
        fields = ["route_category", "route_query", "route", "params"]
        depth = 1


class StackRoutesURLAndParamsSerializer(serializers.Serializer):
    url = serializers.CharField(max_length=100)
    params = serializers.CharField(max_length=250)

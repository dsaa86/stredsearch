from typing import Any

from django.db import models
from django.contrib.auth.models import User


class StackParams(models.Model):
    param_name = models.CharField(max_length=50, blank=False)
    param_description = models.CharField(max_length=150, blank=False)

    def __str__(self) -> str:
        return self.param_name


class StackSortMethods(models.Model):
    sort_name = models.CharField(max_length=50, blank=False)
    sort_description = models.CharField(max_length=150, blank=False)

    def __str__(self) -> str:
        return self.sort_name


class StackOrderMethods(models.Model):
    order_name = models.CharField(max_length=50, blank=False)
    order_description = models.CharField(max_length=150, blank=False)

    def __str__(self) -> str:
        return self.order_name


class StackFilters(models.Model):
    filter_name = models.CharField(max_length=50, blank=False)
    filter_description = models.CharField(max_length=150, blank=False)

    def __str__(self) -> str:
        return self.filter_name


class StackQuestionDataFields(models.Model):
    data_field_name = models.CharField(max_length=50, blank=False)
    data_field_description = models.CharField(max_length=150, blank=False)

    def __str__(self) -> str:
        return self.data_field_name


class StackRoute(models.Model):
    route_category = models.CharField(blank=False, default="", max_length=200)
    route_query = models.CharField(blank=False, default="", max_length=200)
    route = models.CharField(blank=False, default="", max_length=200)
    params = models.ManyToManyField(StackParams)

    def __str__(self) -> str:
        return self.route


class StackRouteMeta(models.Model):
    route_prepend = models.CharField(max_length=200)
    route_append = models.CharField(max_length=200)


class StackUser(models.Model):
    user_id = models.IntegerField(unique=True)
    display_name = models.CharField(max_length=200, blank=True)

    def __str__(self) -> str:
        return self.display_name


class StackTags(models.Model):
    tag_name = models.CharField(max_length=100, blank=False, unique=True)
    number_of_instances_on_so = models.IntegerField(default=0, blank=True)
    number_of_cached_instances = models.IntegerField(default=0, blank=True)

    def __str__(self) -> str:
        return self.tag_name


class SearchTerms(models.Model):
    search_term = models.CharField(max_length=500, null=True, unique=True)

    def __str__(self) -> str:
        return self.search_term


class StredSearchQuestion(models.Model):
    created_on_stredsearch = models.DateTimeField(auto_now_add=True)
    updated_on_stredsearch = models.DateTimeField(auto_now=True)
    search_term = models.ManyToManyField(SearchTerms)
    link = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    times_returned_as_search_result = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.title


class StackQuestion(StredSearchQuestion):
    owner = models.ForeignKey(StackUser, on_delete=models.PROTECT)
    is_answered = models.BooleanField()
    view_count = models.IntegerField()
    answer_count = models.IntegerField()
    score = models.IntegerField()
    last_activity_date = models.DateTimeField()
    creation_date = models.DateTimeField()
    last_edit_date = models.DateTimeField(null=True)
    question_id = models.IntegerField()
    tags = models.ManyToManyField(StackTags, blank=True)

    def __str__(self) -> str:
        return str(self.question_id)


class RedditSearchType(models.Model):
    search_type = models.CharField(max_length=10, blank=False, unique=True)

    def __str__(self) -> str:
        return self.search_type


class RedditSubreddit(models.Model):
    subreddit_name = models.CharField(max_length=100, blank=False, unique=True)

    def __str__(self) -> str:
        return self.subreddit_name


class RedditQuestion(StredSearchQuestion):
    search_type = models.ManyToManyField(RedditSearchType, blank=True)
    subreddit = models.ManyToManyField(RedditSubreddit, blank=True)

    def __str__(self) -> str:
        return self.title


class UserSearchResponses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    search_term = models.ForeignKey(
        SearchTerms, on_delete=models.PROTECT, blank=True, null=True
    )
    stack_responses = models.ManyToManyField(StackQuestion)
    reddit_responses = models.ManyToManyField(RedditQuestion)

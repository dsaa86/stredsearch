from django.db import models


class StackRoute(models.Model):
    route_root = models.CharField(blank=False, default="", max_length=200)
    route = models.CharField(blank=False, default="", max_length=200)
    params = models.JSONField()


class StackMeta(models.Model):
    route_prepend = models.CharField(max_length=200)
    route_append = models.CharField(max_length=200)
    filters = models.JSONField()
    sort = models.JSONField()


class StackUser(models.Model):
    user_id = models.IntegerField()
    display_name = models.CharField(max_length=200)
    gibberish = models.CharField(max_length=500)

    def __str__(self) -> str:
        return self.display_name


class StackTags(models.Model):
    tag_name = models.CharField(max_length=100, blank=False)

    def __str__(self) -> str:
        return self.tag_name


class StackSearchTerms(models.Model):
    search_term = models.CharField(max_length=500, null=True)

    def __str__(self) -> str:
        return self.search_term


class StredSearchQuestion(models.Model):
    created_on_stredsearch = models.DateTimeField(auto_now_add=True)
    updated_on_stredsearch = models.DateTimeField(auto_now=True)
    search_term = models.ManyToManyField(StackSearchTerms)
    link = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    times_returned_as_search_result = models.IntegerField(default=0)


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
        return self.title


class RedditQuestion(StredSearchQuestion):
    type = models.CharField(max_length=10)

from django.db import models


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


class StackRouteMeta(models.Model):
    route_prepend = models.CharField(max_length=200)
    route_append = models.CharField(max_length=200)


class StackUser(models.Model):
    user_id = models.IntegerField()
    display_name = models.CharField(max_length=200)
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
    def getTitle(self):
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
        return super.getTitle(self)
    

class RedditQuestion(StredSearchQuestion):
    type = models.CharField(max_length=10)

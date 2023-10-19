from django.db import models

# Create your models here.

class StackRoute(models.Model):
    route_root = models.CharField(blank=False, default='', max_length=200)
    route = models.CharField(blank=False, default='', max_length=200)
    params = models.JSONField()

class StackMeta(models.Model):
    route_prepend = models.CharField(max_length=200)
    route_append = models.CharField(max_length=200)
    filters = models.JSONField()
    sort = models.JSONField()

class StackUser(models.Model):
    user_id = models.IntegerField()
    display_name = models.CharField(max_length=200)

class StackQuestion(models.Model):
    created_on_stredsearch = models.DateTimeField(auto_now_add=True)
    updated_on_stredsearch = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(StackUser, on_delete=models.PROTECT)
    is_answered = models.BooleanField()
    view_count = models.IntegerField()
    answer_count = models.IntegerField()
    score = models.IntegerField()
    last_activity_date = models.DateTimeField()
    creation_date = models.DateTimeField()
    last_edit_date = models.DateTimeField(blank=True)
    question_id = models.IntegerField()
    link = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
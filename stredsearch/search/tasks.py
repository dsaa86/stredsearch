import time
from datetime import datetime
from re import search

from django_rq import job
from search.tasksextendedfunctionality import *

from .models import *


@job
def insertStackQuestionsToDB(question_set:dict):

    for question in question_set:
        question = removeNaiveTzFromDatetime(question)
        question = createStubsForMissingData(question)
        try:
            question['tags'] = sanitiseTagStringToList(question['tags'])
        except TypeError as e:
            return {"error" : f"TypeError: {e}"}
        if StackQuestion.objects.filter(question_id=question["question_id"]).count() > 0:
            updateQuestionParamsInDB(question)
            continue

        # collect or create all relational objects for the StackQuestion model
        user = retrieveUserFromDB(question['user_id'], question['display_name'])
        try:
            tags = retrieveTagsFromDB(question['tags'])
        except TypeError as e:
            return {"error" : f"TypeError: {e}"}
        search_terms = [retrieveSearchTermFromDB(question)]

        database_question = createNewQuestionInDB(question, user, tags, search_terms)


@job
def commitRedditQuestionsToDB(data:dict):
    pass

@job
def insertStackTagsToDB(data:list):
    for tag in data:
        if StackTags.objects.filter(tag_name=tag).count() > 0:
            tag = StackTags.objects.get(tag_name=tag)
            tag.number_of_instances_on_so = tag['number_of_instances_on_so']
            number_of_cached_instances = StackQuestion.objects.filter(tags__tag_name=tag.tag_name).count()
            tag.number_of_cached_instances = number_of_cached_instances
            tag.save()
        StackTags.objects.create(tag_name=tag["tag_name"], number_of_instances_on_so=tag["number_of_instances_on_so"])

@job
def updateRedditQuestionInDB(data:dict):
    pass

@job
def updateRedditSubRedditsInDb(data:dict):
    pass
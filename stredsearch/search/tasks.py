import time
from datetime import datetime
from os import link
from re import search

from django_rq import job
from search.exceptionhandlers import UnsuccessfulDBSave
from search.tasksextendedfunctionality import *

from .models import *


@job
def insertStackQuestionsToDB(question_set:dict):
    logging.basicConfig(level=logging.DEBUG)
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

        database_question = createNewStackQuestionInDB(question, user, tags, search_terms)


@job
def insertStackTagsToDB(data:list):
    existing_tags = StackTags.objects.all()
    for tag in data:
        if StackTags.objects.filter(tag_name=tag).exists():
            db_tag = StackTags.objects.get(tag_name=tag['tag_name'])
            db_tag.number_of_instances_on_so = tag['number_of_instances_on_so']
            number_of_cached_instances = StackQuestion.objects.filter(tags__tag_name=tag.tag_name).count()
            db_tag.number_of_cached_instances = number_of_cached_instances
            tag.save()
        else:
            StackTags.objects.get_or_create(tag_name=tag["tag_name"], number_of_instances_on_so=tag["number_of_instances_on_so"])



@job
def insertRedditQuestionToDB(data:dict) -> bool:
    search_term = {"q" : data['search_term']}
    question_set = data['question_set']
    type_set = data['search_type_set'].split(",")


    db_search_term = retrieveSearchTermFromDB(search_term)
    for question in question_set:
        
        if not createOrUpdateRedditQuestion(question['link'], question['title'], db_search_term):
            raise UnsuccessfulDBSave
        
        if not addSearchTypeToRedditQuestion(type_set, question['link']):
            raise UnsuccessfulDBSave
        
    return True

import time
from datetime import datetime
from os import link
from re import search

from django_rq import job
from search.tasksextendedfunctionality import *
from search.exceptionhandlers import UnsuccessfulDBSave

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

def createOrUpdateRedditQuestion(link:str, title:str, db_search_term) -> bool:
    db_question_instance = None
    if RedditQuestion.objects.filter(link=link).exists():
        db_question_instance = RedditQuestion.objects.get(link=link)
        db_question_instance.times_returned_as_search_result += 1
    else:
        db_question_instance = RedditQuestion.objects.create(link=link, title=title, times_returned_as_search_result=1)
        db_question_instance.search_term.add(db_search_term)
    try:
        db_question_instance.save()
        return True
    except Exception as e:
        return False

def addSearchTypeToRedditQuestion(type_set: list, link: str) -> bool:
    for search_type in type_set:
        db_question_instance = RedditQuestion.objects.filter(link=link)
        db_type = None
        if RedditSearchType.objects.filter(search_type=search_type).exists():
            db_type = RedditSearchType.objects.get(search_type=search_type)
        else:
            db_type = RedditSearchType.objects.create(search_type=search_type)

        db_question_instance.search_type.add(db_type)
        try:
            db_question_instance.save()
        except Exception as e:
            return False
    return True

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

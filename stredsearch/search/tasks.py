import time
from datetime import datetime
from re import search

from django_rq import job
from search.tasksextendedfunctionality import *

from .models import *


@job
def insertStackQuestionsToDB(question_set:dict):
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("START: insertStackQuestionsToDB")
    logging.debug("insertStackQuestionsToDB - beginning question loop")
    for question in question_set:
        question = removeNaiveTzFromDatetime(question)
        logging.debug("insertStackQuestionsToDB - naive tz completed")
        question = createStubsForMissingData(question)
        logging.debug("insertStackQuestionsToDB - stubs created")
        try:
            question['tags'] = sanitiseTagStringToList(question['tags'])
            logging.debug("insertStackQuestionsToDB - tags sanitised")
        except TypeError as e:
            logging.debug(f"insertStackQuestionsToDB - tags sanitisation failed: {e}")
            return {"error" : f"TypeError: {e}"}
        if StackQuestion.objects.filter(question_id=question["question_id"]).count() > 0:
            logging.debug("insertStackQuestionsToDB - question already exists in DB")
            updateQuestionParamsInDB(question)
            logging.debug("insertStackQuestionsToDB - question params updated")
            continue

        logging.debug("insertStackQuestionsToDB - question does not exist in DB")
        # collect or create all relational objects for the StackQuestion model
        user = retrieveUserFromDB(question['user_id'], question['display_name'])
        logging.debug("insertStackQuestionsToDB - user retrieved")
        try:
            tags = retrieveTagsFromDB(question['tags'])
            logging.debug("insertStackQuestionsToDB - tags retrieved")
        except TypeError as e:
            logging.debug(f"insertStackQuestionsToDB - tags retrieval failed: {e}")
            return {"error" : f"TypeError: {e}"}
        search_terms = [retrieveSearchTermFromDB(question)]

        database_question = createNewQuestionInDB(question, user, tags, search_terms)


@job
def commitRedditQuestionsToDB(data:dict):
    pass

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
def updateRedditQuestionInDB(data:dict):
    pass

@job
def updateRedditSubRedditsInDb(data:dict):
    pass
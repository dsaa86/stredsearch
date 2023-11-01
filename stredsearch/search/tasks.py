import time
from datetime import datetime
from re import search

from django_rq import job

from .models import *
from search.tasksextendedfunctionality import *

# logger = logging.getLogger(__name__)


    
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
def task_execute(data:dict):

    time.sleep(2)

    # INSERT TASKS HERE

    # logger.info(f"{name} start log...")

    # try:
    #     user = StackUser.objects.get(user_id=user_id)
    #     user.gibberish = rand_string
    #     user.save()
    #     print("SUCCESS")
    #     # logger.info("SUCCESS")
    # except Exception as e:
    #     print(e)
    #     # logger.info("ERROR")
    #     # logger.error(e)

@job
def commitStackQuestionsToDB(data:dict):
    pass

@job
def commitRedditQuestionsToDB(data:dict):
    pass

@job
def updateStackQuestionInDB(data:dict):
    pass

@job
def updateStackTagListInDB(data:dict):
    pass

@job
def updateRedditQuestionInDB(data:dict):
    pass

@job
def updateRedditSubRedditsInDb(data:dict):
    pass
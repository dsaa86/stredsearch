import logging
import random
import time
from datetime import datetime
from re import search

from django_rq import job

from .models import *

# logger = logging.getLogger(__name__)

def updateQuestionParamsInDB(question):
    database_instance = StackQuestion.objects.get(question_id=question["question_id"])
    
    database_instance.last_activity_date = max(database_instance.last_activity_date, question["last_activity_date"])
    database_instance.last_edit_date = max(database_instance.last_edit_date, question["last_edit_date"])
    database_instance.is_answered = question["is_answered"]
    database_instance.view_count = max(database_instance.view_count, question["view_count"])
    database_instance.answer_count = max(database_instance.answer_count, question["answer_count"])
    database_instance.score = max(database_instance.score, question["score"])

    if "q" in question.keys():
        search_term = retrieveSearchTermFromDB(question)
        database_instance.search_term = search_term

    if database_instance.save():
        return True
    
def retrieveUserFromDB(user_id, display_name):
    if StackUser.objects.filter(user_id=user_id).count() > 0:
        return StackUser.objects.get(user_id=user_id)
    else:
        return StackUser.objects.create(user_id=user_id, display_name=display_name)
    
def retrieveTagsFromDB(tags):
    tag_list = []
    for tag in tags:
        if StackTags.objects.filter(tag_name=tag).count() > 0:
            tag_list.append(StackTags.objects.get(tag_name=tag))
        else:
            tag_list.append(StackTags.objects.create(tag_name=tag))
    return tag_list

def retrieveSearchTermFromDB(question):

    if "q" in question.keys():
        if StackSearchTerms.objects.filter(search_term=question["q"]).count() > 0:
            return StackSearchTerms.objects.get(search_term=question["q"])
        return StackSearchTerms.objects.create(search_term=question["q"])
    
    if StackSearchTerms.objects.filter(search_term="N/A").count() > 0:
        return StackSearchTerms.objects.get(search_term="N/A")
    return StackSearchTerms.objects.create(search_term="N/A")


def createNewQuestionInDB(question, user, tags, search_term):
    database_question = StackQuestion.objects.create(
        owner=user,
        is_answered=question["is_answered"],
        view_count=question["view_count"],
        answer_count=question["answer_count"],
        score=question["score"],
        last_activity_date=question["last_activity_date"],
        creation_date=question["creation_date"],
        last_edit_date=question["last_edit_date"],
        question_id=question["question_id"],
        search_term=search_term,
        link=question["link"],
        title=question["title"]
    )
    database_question.tags.set(tags)
    database_question.save()
    return database_question


def createStubsForMissingData(question):
    if "last_activity_date" not in question.keys():
        question["last_activity_date"] = datetime.fromtimestamp(946684800)
    if "last_edit_date" not in question.keys():
        question["last_edit_date"] = datetime.fromtimestamp(946684800)
    if "is_answered" not in question.keys():
        question["is_answered"] = False
    if "view_count" not in question.keys():
        question["view_count"] = 0
    if "answer_count" not in question.keys():
        question["answer_count"] = 0
    if "score" not in question.keys():
        question["score"] = 0
    return question

@job
def insertQuestionsToDB(question_set:dict):

    for question in question_set:
        question = createStubsForMissingData(question)
        if StackQuestion.objects.filter(question_id=question["question_id"]).count() > 0:
            updateQuestionParamsInDB(question)
            continue

        # collect or create all relational objects for the StackQuestion model
        user = retrieveUserFromDB(question['user_id'], question['display_name'])
        tags = retrieveTagsFromDB(question['tags'])
        search_term = retrieveSearchTermFromDB(question)

        database_question = createNewQuestionInDB(question, user, tags, search_term)
        print(database_question)



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
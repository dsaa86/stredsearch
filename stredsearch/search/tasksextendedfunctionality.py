from datetime import datetime
from re import search

import pytz

from .models import StackQuestion, StackSearchTerms, StackTags, StackUser


def updateQuestionParamsInDB(question):
    database_instance = StackQuestion.objects.get(question_id=question["question_id"])

    if database_instance.last_activity_date.tzinfo is None or database_instance.last_activity_date.tzinfo.utcoffset(database_instance.last_activity_date) is None:
        database_instance.last_activity_date = pytz.utc.localize(database_instance.last_activity_date)

    if database_instance.last_edit_date.tzinfo is None or database_instance.last_edit_date.tzinfo.utcoffset(database_instance.last_edit_date) is None:
        database_instance.last_edit_date = pytz.utc.localize(database_instance.last_edit_date)

    if question["last_activity_date"].tzinfo is None or question["last_activity_date"].tzinfo.utcoffset(question["last_activity_date"]) is None:
        question["last_activity_date"] = pytz.utc.localize(question["last_activity_date"])

    if question["last_edit_date"].tzinfo is None or question["last_edit_date"].tzinfo.utcoffset(question["last_edit_date"]) is None:
        question["last_edit_date"] = pytz.utc.localize(question["last_edit_date"])

    database_instance.last_activity_date = max(database_instance.last_activity_date, question["last_activity_date"])
    database_instance.last_edit_date = max(database_instance.last_edit_date, question["last_edit_date"])
    database_instance.is_answered = question["is_answered"]
    database_instance.view_count = max(database_instance.view_count, question["view_count"])
    database_instance.answer_count = max(database_instance.answer_count, question["answer_count"])
    database_instance.score = max(database_instance.score, question["score"])

    if "q" in question.keys():
        terms = [retrieveSearchTermFromDB(question)]
        database_instance.search_term.set(terms)

    if database_instance.save():
        return True
    
def retrieveUserFromDB(user_id, display_name):
    if StackUser.objects.filter(user_id=user_id).count() > 0:
        return StackUser.objects.get(user_id=user_id)
    else:
        return StackUser.objects.create(user_id=user_id, display_name=display_name)
    
def retrieveTagsFromDB(tags:list) -> list:

    if not isinstance(tags, list):
        raise TypeError("tags must be of type list")

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


def createNewQuestionInDB(question, user, tags, search_terms):
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
        link=question["link"],
        title=question["title"]
    )
    database_question.search_term.set(search_terms)
    database_question.tags.set(tags)
    database_question.save()
    return database_question


def createStubsForMissingData(question):
    stub_datetime = datetime.now()
    stub_datetime.replace(year=2000, month=1, day=1, hour=0, minute=0, second=0, microsecond=0, tzinfo=pytz.timezone("Asia/Dubai"))
    if "creation_date" not in question.keys():
        question["creation_date"] = stub_datetime
    if "last_activity_date" not in question.keys():
        question["last_activity_date"] = stub_datetime
    if "last_edit_date" not in question.keys():
        question["last_edit_date"] = stub_datetime
    if "is_answered" not in question.keys():
        question["is_answered"] = False
    if "view_count" not in question.keys():
        question["view_count"] = 0
    if "answer_count" not in question.keys():
        question["answer_count"] = 0
    if "score" not in question.keys():
        question["score"] = 0
    if "user_id" not in question.keys():
        question["user_id"] = 111111111
        question["display_name"] = "N/A"
    return question

def removeNaiveTzFromDatetime(question):

    if "last_activity_date" in question.keys() and (question["last_activity_date"].tzinfo is None or question["last_activity_date"].tzinfo.utcoffset(question["last_activity_date"]) is None):
        question["last_activity_date"] = pytz.utc.localize(question["last_activity_date"])

    if "last_edit_date" in question.keys() and (question["last_edit_date"].tzinfo is None or question["last_edit_date"].tzinfo.utcoffset(question["last_edit_date"]) is None):
        question["last_edit_date"] = pytz.utc.localize(question["last_edit_date"])

    if "creation_date" in question.keys() and (question["last_activity_date"].tzinfo is None or question["last_activity_date"].tzinfo.utcoffset(question["last_activity_date"]) is None):
        question["creation_date"] = pytz.utc.localize(question["creation_date"])

    return question


def sanitiseTagStringToList(tag_string:str) -> list:

    if not isinstance(tag_string, str):
        raise TypeError("tag_string must be of type str")

    return tag_string.split(", ")
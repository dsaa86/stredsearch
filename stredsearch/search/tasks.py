import time
from datetime import datetime
from os import link
from re import search

from django import db
from django_rq import job
from search.exceptionhandlers import UnsuccessfulDBSave
from search.tasksextendedfunctionality import *

from .models import *


@job
def insertStackQuestionsToDB(question_set: dict):
    for question in question_set:
        question = removeNaiveTzFromDatetime(question)
        question = createStubsForMissingData(question)
        try:
            question["tags"] = sanitiseTagStringToList(question["tags"])
        except TypeError as e:
            return {"error": f"TypeError: {e}"}
        if (
            StackQuestion.objects.filter(question_id=question["question_id"]).count()
            > 0
        ):
            updateQuestionParamsInDB(question)
            continue

        # collect or create all relational objects for the StackQuestion model
        user = retrieveUserFromDB(question["user_id"], question["display_name"])
        try:
            tags = retrieveTagsFromDB(question["tags"])
        except TypeError as e:
            return {"error": f"TypeError: {e}"}
        search_terms = [retrieveSearchTermFromDB(question)]

        database_question = createNewStackQuestionInDB(
            question, user, tags, search_terms
        )


@job
def insertStackTagsToDB(data: list):
    existing_tags = StackTags.objects.all()
    for tag in data:
        if StackTags.objects.filter(tag_name=tag).exists():
            db_tag = StackTags.objects.get(tag_name=tag["tag_name"])
            db_tag.number_of_instances_on_so = tag["number_of_instances_on_so"]
            number_of_cached_instances = StackQuestion.objects.filter(
                tags__tag_name=tag.tag_name
            ).count()
            db_tag.number_of_cached_instances = number_of_cached_instances
            tag.save()
        else:
            StackTags.objects.get_or_create(
                tag_name=tag["tag_name"],
                number_of_instances_on_so=tag["number_of_instances_on_so"],
            )


@job
def insertRedditQuestionToDB(data: dict) -> bool:
    db_subreddit_list = getRedditSubredditList(data["subreddits"])
    db_search_type_list = getRedditSearchTypeList(data["search_type_set"])
    db_search_term = getRedditSearchTerm(data["search_term"])

    for question in data["question_set"]:
        db_question_instance = None
        if RedditQuestion.objects.filter(link=question["question_link"]).exists():
            db_question_instance = RedditQuestion.objects.get(
                link=question["question_link"]
            )
            db_question_instance.times_returned_as_search_result += 1
        else:
            db_question_instance = RedditQuestion.objects.create(
                link=question["question_link"],
                title=question["question_title"],
                times_returned_as_search_result=1,
            )

        for subreddit in db_subreddit_list:
            if type(subreddit) == tuple:
                db_question_instance.subreddit.add(subreddit[0])
            else:
                db_question_instance.subreddit.add(subreddit)

        for search_type in db_search_type_list:
            if type(search_type) == tuple:
                db_question_instance.search_type.add(search_type[0])
            else:
                db_question_instance.search_type.add(search_type)

        if type(db_search_term) == tuple:
            db_question_instance.search_term.add(db_search_term[0])
        else:
            db_question_instance.search_term.add(db_search_term)

        try:
            db_question_instance.save()
            return True
        except Exception as e:
            raise UnsuccessfulDBSave(f"Unsuccessful DB save: {e}")
            return False

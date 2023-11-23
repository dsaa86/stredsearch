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
    """
    Question --> Reddit Question --> StredSearchQuestion

    1. Search Type --> RedditSearchType == search type
    2. Created On & Updated On == datetime.now()
    3. Search Term  --> Search Terms --> question
    4. Link == Link
    4. Title == Title
    5. Times Returned == 1

    create question set and add to db


    """


@job
def insertRedditQuestionToDB(data: dict) -> bool:
    search_term = data["search_term"]
    question_set = data["question_set"]
    type_set = data["search_type_set"].split(",")
    subreddits = data["subreddit"].split(",")

    print("SEARCH TERM: ", search_term)
    print("QUESTION SET: ", question_set)
    print("TYPE SET: ", type_set)

    db_subreddit_list = []
    for subreddit in subreddits:
        if RedditSubreddit.objects.filter(subreddit_name=subreddit).exists():
            db_subreddit_list.append(
                RedditSubreddit.objects.get(subreddit_name=subreddit)
            )
        else:
            db_subreddit_list.append(
                RedditSubreddit.objects.get_or_create(
                    subreddit_name=subreddit,
                )
            )

    # Get Search Type
    db_search_type_list = []
    for search_type in type_set:
        if RedditSearchType.objects.filter(search_type=search_type).exists():
            db_search_type_list.append(
                RedditSearchType.objects.get(search_type=search_type)
            )
        else:
            db_search_type_list.append(
                RedditSearchType.objects.get_or_create(search_type=search_type)
            )

    # Get SearchTerm
    db_search_term = None
    if SearchTerms.objects.filter(search_term=search_term).exists():
        db_search_term = SearchTerms.objects.get(search_term=search_term)
    else:
        db_search_term = SearchTerms.objects.get_or_create(search_term=search_term)

    for question in question_set:
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
            db_question_instance.search_term.add(db_search_term)
            db_question_instance.search_type.set(db_search_type_list)
            db_question_instance.subreddit.set(db_subreddit_list)
        try:
            db_question_instance.save()
        except Exception as e:
            raise UnsuccessfulDBSave(f"Unsuccessful DB save: {e}")

    return True

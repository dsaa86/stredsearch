from celery import shared_task
import glob
import os
import io
from search.models import *
from django.db.models import F
from django.db.models.query import QuerySet


def getStackUserFromDBOrCreate(question):
    user = None

    try:
        if question["user_id"] in StackUser.objects.values_list("user_id", flat=True):
            user = StackUser.objects.all().filter(user_id=question["user_id"]).first()
        else:
            user = StackUser.objects.create(
                user_id=question["user_id"], display_name=question["display_name"]
            )
    except KeyError as e:
        # User has been deleted from the SO database
        # The search result from the API does not contain user data
        if "StredSearch: StackOverflow User Deleted" in StackUser.objects.values_list(
            "display_name", flat=True
        ):
            user = (
                StackUser.objects.all()
                .filter(display_name="StredSearch: StackOverflow User Deleted")
                .first()
            )
        else:
            user = StackUser.objects.create(
                user_id=00000000, display_name="StredSearch: StackOverflow User Deleted"
            )

    return user


def getStackSearchTermFromDBOrCreate(search_term):
    search_term_db_obj = None

    if search_term in StackSearchTerms.objects.values_list("search_term", flat=True):
        search_term_db_obj = StackSearchTerms.objects.all().filter(
            search_term=search_term
        )
    elif search_term != None:
        search_term_db_obj = StackSearchTerms.objects.create(search_term=search_term)

    return search_term_db_obj


def getStackTagsFromDBOrCreate(question):
    tags_list = question["tags"].split(",")

    all_tags_in_db = StackTags.objects.values_list("tag_name", flat=True)

    tags_objs = []

    for tag in tags_list:
        if tag in all_tags_in_db:
            tags_objs.append(StackTags.objects.all().filter(tag_name=tag))
        else:
            tags_objs.append(StackTags.objects.create(tag_name=tag))

    return tags_objs


@shared_task(name="asyncStackQuestionDBProcessor")
def asyncStackQuestionDBProcessor(questions_passed, search_term):
    questions = questions_passed

    for question in questions:
        # Is the question already in the DB? If so, increment the
        # 'times_viewed' counter by 1.
        if question["question_id"] in StackQuestion.objects.values_list(
            "question_id", flat=True
        ):
            StackQuestion.objects.all().filter(
                question_id=question["question_id"]
            ).update(
                times_returned_as_search_result=F("times_returned_as_search_result") + 1
            )
            continue

        user = getStackUserFromDBOrCreate(question)

        search_term_db_obj = getStackSearchTermFromDBOrCreate(search_term)

        tags_objs = getStackTagsFromDBOrCreate(question)

        question_to_add_to_db = StackQuestion.objects.create(
            is_answered=question["is_answered"],
            view_count=question["view_count"],
            answer_count=question["answer_count"],
            score=question["score"],
            last_activity_date=question["last_activity_date"],
            creation_date=question["creation_date"],
            question_id=question["question_id"],
            owner=user,
            title=question["title"],
            times_returned_as_search_result=1,
        )

        # Existing tags returned as type QuerySet, new tags returned as part
        # of the question (ultimately this is from the HTTP response from SO)
        for tag_obj in tags_objs:
            if type(tag_obj) is QuerySet:
                question_to_add_to_db.tags.add(tag_obj.values()[0]["id"])
            else:
                question_to_add_to_db.tags.add(tag_obj.id)

        # Not all questions have a last edit date
        if "last_edit_date" in question.keys():
            question_to_add_to_db.last_edit_date = question["last_edit_date"]

        # Search terms only exist in advanced searches, all other SO searches
        # are based on tags alone.
        if search_term_db_obj != None:
            question_to_add_to_db.search_term = search_term_db_obj

        question_to_add_to_db.save()

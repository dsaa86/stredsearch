from celery import shared_task
import glob
import os
import io
from search.models import *
from django.db.models import F
from django.db.models.query import QuerySet


# FIXME Needs refactoring in to segregated functions | CREATED: 18:49 23/10/2023


@shared_task
def tasksReceiver(questions_passed, search_term):
    questions = questions_passed

    for question in questions:
        if question["question_id"] in StackQuestion.objects.values_list(
            "question_id", flat=True
        ):
            StackQuestion.objects.all().filter(
                question_id=question["question_id"]
            ).update(
                times_returned_as_search_result=F("times_returned_as_search_result") + 1
            )
            continue

        user = None

        if question["user_id"] in StackUser.objects.values_list("user_id", flat=True):
            user = StackUser.objects.all().filter(user_id=question["user_id"]).first()
        else:
            user = StackUser.objects.create(
                user_id=question["user_id"], display_name=question["display_name"]
            )

        search_term_db_obj = None

        if search_term in StackSearchTerms.objects.values_list(
            "search_term", flat=True
        ):
            search_term_db_obj = StackSearchTerms.objects.all().filter(
                search_term=search_term
            )
        elif search_term != None:
            search_term_db_obj = StackSearchTerms.objects.create(
                search_term=search_term
            )

        tags_list = question["tags"].split(",")

        all_tags_in_db = StackTags.objects.values_list("tag_name", flat=True)

        tags_objs = []

        for tag in tags_list:
            if tag in all_tags_in_db:
                tags_objs.append(StackTags.objects.all().filter(tag_name=tag))
            else:
                tags_objs.append(StackTags.objects.create(tag_name=tag))

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

        for tag_obj in tags_objs:
            if type(tag_obj) is QuerySet:
                question_to_add_to_db.tags.add(tag_obj.values()[0]["id"])
            else:
                question_to_add_to_db.tags.add(tag_obj.id)

        if "last_edit_date" in question.keys():
            question_to_add_to_db.last_edit_date = question["last_edit_date"]

        if search_term_db_obj != None:
            question_to_add_to_db.search_term = search_term_db_obj

        question_to_add_to_db.save()

        print("Success")

    all_users = StackUser.objects.all()

    for user in all_users:
        print(user)

    all_questions = StackQuestion.objects.all()

    for question in all_questions:
        print(question)

    all_tags = StackTags.objects.all()

    for tag in all_tags:
        print(tag)

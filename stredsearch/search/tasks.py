import time
from datetime import datetime
from re import search

from django_rq import job
from search.tasksextendedfunctionality import *

from .models import *


@job
def insertStackQuestionsToDB(question_set:dict):
    logging.basicConfig(level=logging.DEBUG)
    # logging.debug("START: insertStackQuestionsToDB")
    # logging.debug("insertStackQuestionsToDB - beginning question loop")
    for question in question_set:
        question = removeNaiveTzFromDatetime(question)
        # logging.debug("insertStackQuestionsToDB - naive tz completed")
        question = createStubsForMissingData(question)
        # logging.debug("insertStackQuestionsToDB - stubs created")
        try:
            question['tags'] = sanitiseTagStringToList(question['tags'])
            # logging.debug("insertStackQuestionsToDB - tags sanitised")
        except TypeError as e:
            # logging.debug(f"insertStackQuestionsToDB - tags sanitisation failed: {e}")
            return {"error" : f"TypeError: {e}"}
        if StackQuestion.objects.filter(question_id=question["question_id"]).count() > 0:
            # logging.debug("insertStackQuestionsToDB - question already exists in DB")
            updateQuestionParamsInDB(question)
            # logging.debug("insertStackQuestionsToDB - question params updated")
            continue

        # logging.debug("insertStackQuestionsToDB - question does not exist in DB")
        # collect or create all relational objects for the StackQuestion model
        user = retrieveUserFromDB(question['user_id'], question['display_name'])
        # logging.debug("insertStackQuestionsToDB - user retrieved")
        try:
            tags = retrieveTagsFromDB(question['tags'])
            # logging.debug("insertStackQuestionsToDB - tags retrieved")
        except TypeError as e:
            # logging.debug(f"insertStackQuestionsToDB - tags retrieval failed: {e}")
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
def insertRedditQuestionToDB(data:dict):
    logging.basicConfig(level=logging.DEBUG)
    search_term = {"q" : data['search_term']}
    question_set = data['question_set']
    type_set = data['search_type_set'].split(",")

    logging.debug(f"{type_set}")

    db_search_term = retrieveSearchTermFromDB(search_term)
    logging.debug(f"DB Search Term: {db_search_term}")
    for question in question_set:
        db_question_instance = None
        if RedditQuestion.objects.filter(link=question['link']).exists():
            logging.debug(f"Question {question['link']} already exists in DB")
            db_question_instance = RedditQuestion.objects.get(link=question['link'])
            db_question_instance.times_returned_as_search_result += 1
            db_question_instance.save()
            logging.debug("Question times returned as search result updated")
        else:
            db_question_instance = RedditQuestion.objects.create(link=question['link'], title=question['title'], times_returned_as_search_result=1)
            db_question_instance.search_term.add(db_search_term)
            db_question_instance.save()

        logging.debug("Setting search_type")
        for search_type in type_set:
            logging.debug(f"Search_type: {search_type}")
            if RedditSearchType.objects.filter(search_type=search_type).exists():
                logging.debug("Search type already exists")
                db_type = RedditSearchType.objects.get(search_type=search_type)
                db_question_instance.search_type.add(db_type)
            else:
                logging.debug("Search type does not exist yet")
                db_type = RedditSearchType.objects.create(search_type=search_type)
                db_question_instance.search_type.add(db_type)
        db_question_instance.save()
        logging.debug("Search type added, and saved")


@job
def updateRedditSubRedditsInDb(data:dict):
    pass
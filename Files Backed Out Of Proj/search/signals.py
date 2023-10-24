from django.dispatch import Signal
from search.tasks import asyncStackQuestionDBProcessor

# from stredsearch.celery import commitStackQuestionsToDB


commit_questions_to_local_db_signal = Signal()

from search.signals import commit_questions_to_local_db_signal


# def commitNewQuestion(sender, questions, search_term, **kwargs):
# asyncStackQuestionDBProcessor.apply_async(args=[questions, search_term])
# commitStackQuestionsToDB(questions, search_term).apply_async()

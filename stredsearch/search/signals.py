from django.dispatch import Signal
from search.tasks import asyncStackQuestionDBProcessor


commit_questions_to_local_db_signal = Signal()

from search.signals import commit_questions_to_local_db_signal


def commitNewQuestion(sender, questions, search_term, **kwargs):
    asyncStackQuestionDBProcessor(questions, search_term)

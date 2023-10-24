# from __future__ import absolute_import, unicode_literals
# import os

# import django
# from celery import Celery
# from django.conf import settings
#
# from search.tasks import getStackSearchTermFromDBOrCreate

# app = Celery("stredsearch")
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stredsearch.settings")
# app.conf.enable_utc = False

# app.config_from_object("django.conf:settings", namespace="CELERY")
# app.autodiscover_tasks()


# @app.task(bind=True)
# def debug_task(self):
#     print(f"Request: {self.request!r}")


# @app.task(bind=True)
# def commitStackQuestionsToDB(questions, search_term):
#     return getStackSearchTermFromDBOrCreate(questions, search_term)


import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stredsearch.settings")

app = Celery("stredsearch")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

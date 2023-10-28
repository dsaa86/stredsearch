import random
import time

from django_rq import job
import logging

from .models import *

# logger = logging.getLogger(__name__)


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

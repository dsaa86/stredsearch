import random
import time

from django_rq import job
import logging

from .models import *

# logger = logging.getLogger(__name__)


@job
def task_execute(data:dict):

    time.sleep(2)

    display_name = data["display_name"]
    user_id = data["user_id"]

    alphabet = [
        "a",
        "b",
        "c",
        "d",
        "e",
        " f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
    ]
    rand_string = ""

    for x in range(0, 400):
        letter = alphabet[random.randint(0, 25)]
        rand_string += letter

    print(rand_string)

    # logger.info(f"{name} start log...")

    try:
        user = StackUser.objects.get(user_id=user_id)
        user.gibberish = rand_string
        user.save()
        print("SUCCESS")
        # logger.info("SUCCESS")
    except Exception as e:
        print(e)
        # logger.info("ERROR")
        # logger.error(e)

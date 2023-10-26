import random

from django_rq import job
import logging

from .models import *

# logger = logging.getLogger(__name__)


@job
def task_execute(name):
    print("Working Nicely")

    # alphabet = [
    #     "a",
    #     "b",
    #     "c",
    #     "d",
    #     "e",
    #     " f",
    #     "g",
    #     "h",
    #     "i",
    #     "j",
    #     "k",
    #     "l",
    #     "m",
    #     "n",
    #     "o",
    #     "p",
    #     "q",
    #     "r",
    #     "s",
    #     "t",
    #     "u",
    #     "v",
    #     "w",
    #     "x",
    #     "y",
    #     "z",
    # ]
    # rand_string = ""

    # for x in range(0, 500):
    #     letter = alphabet[random.randint(0, 25)]
    #     rand_string += letter

    # # logger.info(f"{name} start log...")

    # try:
    #     user = StackUser.objects.get(name=name)
    #     user.gibberish = rand_string
    #     user.save()
    #     print("SUCCESS")
    #     # logger.info("SUCCESS")
    # except Exception as e:
    #     print(e)
    #     # logger.info("ERROR")
    #     # logger.error(e)

from celery import shared_task
import random

from .models import *


@shared_task()
def task_execute(name):
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

    for x in range(0, 500):
        letter = alphabet[random.randint(0, 25)]
        rand_string += letter

    user = StackUser.objects.get(name=name)
    user.gibberish = rand_string

    user.save()

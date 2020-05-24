#!/usr/bin/python
# coding=utf-8
"""Load test KanyAI using the Locust library.

:usage:
    To be run with every commit
:authors
    MD at 03/01/20
"""
from locust import HttpLocust, TaskSet, between
import random
import string


def get_song(locust):
    """Generate a song by sending a random string of length 2-100 to the index page."""
    text_input = ''.join(random.choice(string.ascii_letters) for _ in range(random.randint(2, 100)))
    data = {'input': text_input}
    locust.client.post("/", data)


class GetSong(TaskSet):
    """Locust Task set to log on to site and get a song."""

    tasks = {get_song: 1}


class WebsiteUser(HttpLocust):
    """Main locust class."""

    task_set = GetSong
    wait_time = between(5.0, 9.0)

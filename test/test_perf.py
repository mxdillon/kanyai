#!/usr/bin/python
# coding=utf-8
""" Test performance of application
:usage:
    To be run with every commit
:authors
    JP at 04/01/20
"""
import time


def test_post(client):
    """Check the index page loads."""
    start = time.time()
    form_data = {'text_input': 'test song'}
    response = client.post('/', data=form_data)
    elapsed = time.time() - start
    print(f'elapsed time for request is {elapsed}')
    assert response.status_code == 200, "Response not ok"
    # Setting a 20 second limit for responses - this is a finger in the air guess
    assert elapsed < 20, "Request too slow"

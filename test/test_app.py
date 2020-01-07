#!/usr/bin/python
# coding=utf-8
""" Tests for KanyAI application
:usage:
    Run with every commit.
:authors
    JP at 02/01/20
"""


def test_health(env_setup, client):
    """Check the health of the service."""
    response = client.get('health')
    assert response.json == {"Status": 'OK'}


def test_index(client):
    """Check the index page loads."""
    response = client.get('/')
    assert response.status_code == 200


def test_post(client):
    """Check the post request for generating lyrics."""
    response = client.post('/')
    assert response.status_code == 200


def test_greatest_hits(client):
    """Check the get request for generating the greatest hits."""
    response = client.get('/greatest-hits')
    assert response.status_code == 200

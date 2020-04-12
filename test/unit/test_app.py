#!/usr/bin/python
# coding=utf-8
"""Tests for KanyAI application.

:usage:
    Run with every commit.
:authors
    JP at 02/01/20
"""
import os


def test_model_exists():
    """Check the model file is the expected location"""
    assert os.path.isfile("./model/gpt2-simple/model-690.data-00000-of-00001"), "Model file doesn't exist"


def test_health(client):
    """Check the health of the service."""
    response = client.get('health')
    assert response.json == {"Status": 'OK'}


def test_index(client):
    """Check the index page loads."""
    response = client.get('/')
    assert response.status_code == 200


def test_post(client):
    """Check the post request for generating lyrics."""
    response = client.post('/', data={'text_input': 'test'})
    assert response.status_code == 200

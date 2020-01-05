#!/usr/bin/python
# coding=utf-8
""" Tests for KanyAI application
:usage:
    Run with every commit.
:authors
    JP at 02/01/20
"""
import pytest


@pytest.mark.usefixtures('env_setup', 'client')
def test_health(env_setup, client):
    """Check the health of the service."""
    response = client.get('health')
    assert response.json == {"Status": 'OK'}


@pytest.mark.usefixtures('client')
def test_index(client):
    """Check the index page loads."""
    response = client.get('/')
    assert response.status_code == 200


@pytest.mark.usefixtures('client')
def test_post(client):
    """Check the post request for generating lyrics."""
    response = client.post('/')
    assert response.status_code == 200

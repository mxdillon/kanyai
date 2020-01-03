#!/usr/bin/python
# coding=utf-8
""" Tests for KanyAI application
:usage:
    Run with every commit.
:authors
    JP at 02/01/20
"""
import pytest


@pytest.mark.usefixtures('client')
def test_health(client):
    """Check the health of the service."""
    response = client.get('health')
    assert response.json == {"Status": 'OK'}


@pytest.mark.usefixtures('client')
def test_index(client):
    """Check the index page loads."""
    response = client.get('/')
    assert response.status_code == 200

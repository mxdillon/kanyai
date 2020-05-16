#!/usr/bin/python
# coding=utf-8
"""Fixtures for all tests.

:usage:
    To be run with every commit
:authors
    MD at 03/01/20
"""

import pytest
from app import generate_lyrics
from app import server


@pytest.fixture
def mock_get_input(monkeypatch):
    """Requests.get() mocked to return {'mock_key':'mock_response'}."""

    def mock_get_input(request=None):
        return "test song"

    monkeypatch.setattr(server, 'get_input', mock_get_input)


@pytest.fixture(scope='session')
def generator():
    """Get the Generator class for the GPT NLG model."""
    return generate_lyrics.GenerateLyrics(model_folder='gpt2-simple', checkpoint_directory='/tmp/model')

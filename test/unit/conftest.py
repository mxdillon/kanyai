#!/usr/bin/python
# coding=utf-8
"""Fixtures for all tests.

:usage:
    To be run with every commit
:authors
    MD at 03/01/20
"""

import pytest
from app.ml.generate_lyrics import GenerateLyrics
from app.server import get_generator


@pytest.fixture(scope='session')
def client():
    """Flask test client with Google Cloud logging client removed."""
    from main import create_app
    app = create_app()
    client = app.test_client()
    return client


@pytest.fixture(scope='session')
def generator_class():
    """Get the Generator class for the GPT NLG model."""
    return GenerateLyrics(model_folder='gpt2-simple', checkpoint_directory='model')


@pytest.fixture(scope='session')
def generator():
    """Check we can get the lyric generator object, which loads the model."""
    return get_generator(model_folder='gpt2-simple', checkpoint_directory='model')

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


@pytest.fixture
def client():
    """Flask test client with Google Cloud logging client removed."""
    from main import create_app
    app = create_app()
    client = app.test_client()
    return client


@pytest.fixture(scope='session')
def generator_class():
    return GenerateLyrics(embedding_dim=512)


@pytest.fixture(scope='session')
def load_maps(generator_class):
    generator_class.load_character_maps(
        character_map_load_path='./test/mock-data/character_index_map.json',
        index_map_load_path='./test/mock-data/index_character_map.npy')
    return generator_class


@pytest.fixture(scope='session')
def rebuild_model(load_maps):
    load_maps.rebuild_model(batch_size=1,
                            weights_path='./test/mock-data/ckpt_')
    return load_maps


@pytest.fixture(scope='session')
def generator():
    """Check we can get the lyric generator object, which loads the model"""
    generator = get_generator(weights_path='./model/ckpt_')
    return generator

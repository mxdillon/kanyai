#!/usr/bin/python
# coding=utf-8
"""Fixtures for all tests.
:usage:
    To be run with every commit
:authors
    MD at 03/01/20
"""

import os
import pytest
import logging
from google.cloud.logging.client import Client
from src.ml.generate_lyrics import GenerateLyrics


@pytest.fixture(autouse=True)
def env_setup(monkeypatch):
    """Mock the credentials environment variable for when the Google logging client is initialised."""
    monkeypatch.setenv('GOOGLE_APPLICATION_CREDENTIALS',
                       './test/mock-data/sample-creds.json')


@pytest.fixture
def client():
    """Flask test client with Google Cloud logging client removed."""
    from app import create_app
    app = create_app()
    client = app.test_client()

    # Remove the Google Cloud logging client for local tests
    test_logger = logging.getLogger()
    for handler in test_logger.handlers:
        if hasattr(handler, 'client'):
            if isinstance(handler.client, Client):
                test_logger.removeHandler(handler)

    return client


@pytest.fixture(scope='session')
def generator_class():
    return GenerateLyrics(embedding_dim=512)


@pytest.fixture(scope='session')
def load_maps(generator_class):
    generator_class.load_character_maps(
        character_map_load_path='../model/character_index_map.json',
        index_map_load_path='../model/index_character_map.npy')
    return generator_class


@pytest.fixture(scope='session')
def rebuild_model(load_maps):
    load_maps.rebuild_model(batch_size=1,
                            weights_path='../model/ckpt_')
    return load_maps

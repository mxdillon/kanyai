#!/usr/bin/python
# coding=utf-8
"""Test machine learning class from generate_lyrics.py
:usage:
    To be run with every commit
:authors
    MD at 06/01/20
"""
import pytest
from src.ml.generate_lyrics import GenerateLyrics


@pytest.fixture(scope='session')
def generator_class():
    return GenerateLyrics(embedding_dim=512)


@pytest.fixture(scope='session')
def load_maps(generator_class):
    generator_class.load_character_maps(
        character_map_load_path='./model/2_noheaders/character_index_map.json',
        index_map_load_path='./model/2_noheaders/index_character_map.npy')


@pytest.fixture(scope='session')
def rebuild_model(load_maps):
    load_maps.rebuild_model(batch_size=1,
                            weights_path='./model/2_noheaders/ckpt_60')

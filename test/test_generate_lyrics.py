#!/usr/bin/python
# coding=utf-8
"""Test generate_lyrics classes and methods
:usage:
    To be run with every commit
:authors
    MD at 03/01/20
"""

import pytest
from app.config.profanity import custom_badwords
from app.ml.generate_lyrics import CleanOutput


def test_character_map_loaded(load_maps):
    assert load_maps.char_to_ind_map is not None


def test_index_map_loaded(load_maps):
    assert load_maps.ind_to_char_map is not None


def test_model_rebuilt(rebuild_model):
    assert rebuild_model is not None


@pytest.mark.parametrize("text_in,expected", [('hello World', 'Hello World'),
                                              ('Hello world', 'Hello world'),
                                              (' what Up', 'What Up'),
                                              (' What Up', 'What Up')])
def test_capitalise_first_character(text_in, expected):
    assert CleanOutput.capitalise_first_character(text_in=text_in) == expected


@pytest.mark.parametrize("text_in,expected", [('hello World', 'hello World '),
                                              (' What Up ', ' What Up ')])
def test_ensure_space(text_in, expected):
    assert CleanOutput.ensure_space(text_in=text_in) == expected


@pytest.mark.parametrize("text_in,expected", [('fuck shit', '**** ****'),
                                              ('hi bitches', 'hi ****es'),
                                              ('nigglsjk asldfjfuck', '****lsjk asldfj****'),
                                              ('BItch fUCk', '**** ****')])
def test_sanitise_string(text_in, expected):
    """Check that custom profanities are being redacted."""
    assert CleanOutput.sanitise_string(text_in=text_in, custom_badwords=custom_badwords) == expected

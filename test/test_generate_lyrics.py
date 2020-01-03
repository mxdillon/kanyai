#!/usr/bin/python
# coding=utf-8
""" Test generate_lyrics classes and methods
:usage:
    To be run with every commit
:authors
    MD at 03/01/20
"""
import pytest
from src.ml.generate_lyrics import remove_start_phrase, capitalise_first_character


@pytest.mark.parametrize("text_in,start_phrase,expected", [('hello world', 'hello', ' world'),
                                                           ('Go! over!', 'Go', '! over!'),
                                                           (' space start', ' spa', 'ce start')])
def test_remove_start_phrase(text_in, start_phrase, expected):
    assert remove_start_phrase(text_in=text_in, start_phrase=start_phrase) == expected


@pytest.mark.parametrize("text_in,expected", [('hello world', 'Hello world'),
                                              ('Hello world', 'Hello world'),
                                              (' what up', 'What up'),
                                              (' What up', 'What up')])
def test_remove_start_phrase(text_in, expected):
    assert capitalise_first_character(text_in=text_in) == expected

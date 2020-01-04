#!/usr/bin/python
# coding=utf-8
""" Test generate_lyrics classes and methods
:usage:
    To be run with every commit
:authors
    MD at 03/01/20
"""
import pytest
from src.ml.generate_lyrics import remove_start_phrase, capitalise_first_character, ensure_space


@pytest.mark.parametrize("text_in,start_phrase,expected", [('hello world', 'hello', ' world'),
                                                           ('Go! over!', 'Go', '! over!'),
                                                           (' space start', ' spa', 'ce start')])
def test_remove_start_phrase(text_in, start_phrase, expected):
    assert remove_start_phrase(text_in=text_in, start_phrase=start_phrase) == expected


@pytest.mark.parametrize("text_in,expected", [('hello World', 'Hello World'),
                                              ('Hello world', 'Hello world'),
                                              (' what Up', 'What Up'),
                                              (' What Up', 'What Up')])
def test_capitalise_first_character(text_in, expected):
    assert capitalise_first_character(text_in=text_in) == expected


@pytest.mark.parametrize("text_in,expected", [('hello World', 'hello World '),
                                              (' What Up ', ' What Up ')])
def test_ensure_space(text_in, expected):
    assert ensure_space(text_in=text_in) == expected

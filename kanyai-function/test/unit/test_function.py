#!/usr/bin/python
# coding=utf-8
"""Tests for KanyAI application.

:usage:
    Run with every commit.
:authors
    JP at 02/01/20
"""
from app import server
from main import get_lyrics


def test_get_input(mock_get_input):
    """A test to check the monkeypatching works properly."""
    song_input = server.get_input()
    assert song_input == "test song"


def test_get_lyrics(mock_get_input):
    """Check the get_lyrics main function generates a song."""
    clean_text = get_lyrics(None)
    assert len(clean_text) > 100

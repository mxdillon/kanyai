#!/usr/bin/python
# coding=utf-8
"""Test server functions to get a song.

:usage:
    To be run with every commit
:authors
    JP at 23/02/20
"""

from app.server import get_text


def test_get_text(client, generator):
    """Check we can get a song (str), it's a generator and that it's longish."""
    with client.application.app_context():
        test_lyric_length = 30
        lines = get_text(text_input='test song', num_words=test_lyric_length, generator=generator)
        print(lines)
        assert isinstance(lines, str)

        song = [line for line in lines]
        assert len(song) > test_lyric_length

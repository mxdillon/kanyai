#!/usr/bin/python
# coding=utf-8
"""Test server functions to get a song
:usage:
    To be run with every commit
:authors
    JP at 23/02/20
"""
import typing
from app.server import get_text


def test_get_text(client, generator):
    """Check we can get a song, it's a generator and that it's longish"""
    with client.application.app_context():
        lines = get_text('test song', generator)
        assert isinstance(lines, typing.Generator)

        song = [line for line in lines]
        assert len(song) > 6

#!/usr/bin/python
# coding=utf-8
"""Test server functions to get a song
:usage:
    To be run with every commit
:authors
    JP at 23/02/20
"""
import typing
from app.ml.generate_lyrics import GenerateLyrics
from app.server import get_text, get_generator


def test_get_text(client):
    """Check we can get a song, it's a generator and that it's longish"""
    with client.application.app_context():
        lines = get_text('test song')
        assert isinstance(lines, typing.Generator)

        song = [line for line in lines]
        assert len(song) > 6


def test_get_generator(client):
    """Check we can get the lyric generator object, which loads the model"""
    with client.application.app_context():
        generator = get_generator(weights_path='./model/ckpt_')
        assert isinstance(generator, GenerateLyrics)

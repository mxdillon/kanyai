#!/usr/bin/python
# coding=utf-8
"""Test server functions to get a song
:usage:
    To be run with every commit
:authors
    JP at 23/02/20
"""
import types
from app.server import get_text, get_generator, stream_text
from app.ml.generate_lyrics import GenerateLyrics


def test_get_text():
    """Check we can get a song, it's a string and that it's long enough"""
    song = get_text('test song')
    assert isinstance(song, str)
    assert len(song) > 400


def test_get_generator():
    """Check we can get the lyric generator object, which loads the model"""
    generator = get_generator(weights_path='./model/ckpt_')
    assert isinstance(generator, GenerateLyrics)


def test_stream_text_type():
    """Check the stream text method returns a song generator"""
    song_generator = stream_text('this is a song about streaming')
    assert isinstance(song_generator, types.GeneratorType), "Expecting a generator from stream text"


def test_stream_text_song_length():
    """Check the stream text method returns a song of length 16"""
    song = [line for line in stream_text('this is a song about streaming')]
    assert len(song) == 16, f"Expecting a song of length 16, got {len(song)}"

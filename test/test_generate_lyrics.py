#!/usr/bin/python
# coding=utf-8
"""Test generate_lyrics classes and methods
:usage:
    To be run with every commit
:authors
    MD at 03/01/20
"""


def test_character_map_loaded(load_maps):
    assert load_maps.char_to_ind_map is not None


def test_index_map_loaded(load_maps):
    assert load_maps.ind_to_char_map is not None


def test_model_rebuilt(rebuild_model):
    assert rebuild_model is not None

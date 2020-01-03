#!/usr/bin/python
# coding=utf-8
""" Flask server
:usage:
    Routes for KanyAI server - healthc heck and index.
:authors
    JP/CW at 02/01/20
"""
from src.ml.generate_lyrics import call_generator, sanitise_string
import logging


def get_text(text_input: str) -> str:
    """Generate the lyrics for the text input from the model.

    :param text_input: starting lyric from the input form
    :return: sanitised lyrics for rendering (str)
    """
    if text_input is None:
        return ' '
    else:
        logging.info(f'Generating lyrics for {text_input}')

        gen_text = call_generator(start_phrase=text_input,
                                  weights_path='./model/1_2la512-256emb512lr003/ckpt_50',
                                  string_length=500)
        gen_text = sanitise_string(text_in=gen_text)
        gen_text = gen_text.replace('\n', '<br>')

        logging.info(f'Generated the song {gen_text}')

        return gen_text

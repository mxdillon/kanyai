#!/usr/bin/python
# coding=utf-8
""" Flask server
:usage:
    Routes for KanyAI server - health check and index.
:authors
    JP/CW at 02/01/20
"""
from src.config.profanity import custom_badwords
from src.ml.generate_lyrics import call_generator, sanitise_string, capitalise_first_character, \
    ensure_space
import logging
import json


def get_text(text_input: str) -> str:
    """Generate the lyrics for the text input from the model.

    :param text_input: starting lyric from the input form
    :return: sanitised lyrics for rendering (str)
    """
    if text_input is None:
        return ' '
    else:
        logging.info(f'Generating lyrics for {text_input}')

        logging.debug(f'ensuring space for {text_input}')
        start_phrase = ensure_space(text_input)

        logging.debug(f'calling generator')
        gen_text = call_generator(start_phrase=start_phrase,
                                  weights_path='./model/3_sanitised80chars/ckpt_75',
                                  string_length=500)
        logging.debug(f'sanitising string')
        gen_text = sanitise_string(text_in=gen_text, custom_badwords=custom_badwords)

        logging.debug(f'capitalising_first_character')
        gen_text = capitalise_first_character(text_in=gen_text)

        logging.debug(f'replacing newlines with linebreaks')
        gen_text = gen_text.replace('\n', '<br>')

        logging.info(f'Generated the song {gen_text}')

        return gen_text

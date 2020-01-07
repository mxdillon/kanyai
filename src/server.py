#!/usr/bin/python
# coding=utf-8
""" Flask server
:usage:
    Routes for KanyAI server - health check and index.
:authors
    JP/CW at 02/01/20
"""
from src.ml.generate_lyrics import call_generator, sanitise_string, remove_start_phrase, capitalise_first_character, \
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
                                  weights_path='./model/2_noheaders/ckpt_60',
                                  string_length=500)
        logging.debug(f'sanitising string')
        gen_text = sanitise_string(text_in=gen_text)

        logging.debug(f'removing start phrase')
        gen_text = remove_start_phrase(text_in=gen_text, start_phrase=start_phrase)

        logging.debug(f'capitalising_first_character')
        gen_text = capitalise_first_character(text_in=gen_text)

        logging.debug(f'replacing newlines with linebreaks')
        gen_text = gen_text.replace('\n', '<br>')

        logging.info(f'Generated the song {gen_text}')

        return gen_text


def get_greatest_hits() -> list:
    """Read the greatest hits json and return results as a list.

    :return: greatest hits (list)
    """
    with open('./static/greatest_hits.json', 'r') as f:
        greatest_hits = json.load(f)
    return greatest_hits

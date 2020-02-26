#!/usr/bin/python
# coding=utf-8
""" Flask server
:usage:
    Routes for KanyAI server - health check and index.
:authors
    JP/CW at 02/01/20
"""
from app.config.profanity import custom_badwords
from app.ml.generate_lyrics import GenerateLyrics
from app.ml.clean_output import CleanOutput
import logging
import typing


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
        start_phrase = CleanOutput.ensure_space(text_input)

        generator = get_generator(weights_path='./model/ckpt_')

        logging.debug('generating text')
        generated_text = generator.generate_text(start_string=start_phrase,
                                                 num_characters=500,
                                                 temperature=0.87)

        logging.debug(f'sanitising string')
        gen_text = CleanOutput.sanitise_string(text_in=generated_text, custom_badwords=custom_badwords)

        logging.debug(f'capitalising_first_character')
        gen_text = CleanOutput.capitalise_first_character(text_in=gen_text)

        logging.debug(f'replacing newlines with linebreaks')
        gen_text = gen_text.replace('\n', '<br>')

        logging.info(f'Generated the song {gen_text}')

        return gen_text


def get_generator(weights_path: str) -> GenerateLyrics:
    """Instantiate the generator class with a saved model and generate a lyrics string.

    :param weights_path: path to the model file containing the weights
    :return: string of generated lyrics appended to the start phrase
    """

    logging.debug('loading GenerateLyrics')
    generator = GenerateLyrics(embedding_dim=512)

    logging.debug('loading character maps')
    generator.load_character_maps(
        character_map_load_path='./model/character_index_map.json',
        index_map_load_path='./model/index_character_map.npy')

    logging.debug('rebuilding model')
    generator.rebuild_model(batch_size=1,
                            weights_path=weights_path)

    generator.model.reset_states()

    return generator


def stream_text(text_input: str) -> typing.Generator:
    """Generate the lyrics for the text input from the model.
    - Get 16 lines as 4 paragraphs

    :param text_input: starting lyric from the input form
    :return: sanitised lyrics for rendering (str)
    """

    generator = get_generator(weights_path='./model/ckpt_')

    logging.debug('loading character maps')
    generator.load_character_maps(
        character_map_load_path='./model/character_index_map.json',
        index_map_load_path='./model/index_character_map.npy')

    next_input = text_input

    for line in range(16):

        gen_text = generator.generate_line(start_string=next_input, temperature=0.87)

        if len(gen_text) < 3:
            continue

        next_input = gen_text

        gen_text = CleanOutput.sanitise_string(text_in=gen_text, custom_badwords=custom_badwords)
        gen_text = CleanOutput.clean_line(text_in=gen_text)
        gen_text = gen_text + '<br>'

        # Return a break before the first line
        if line == 1:
            yield '<br>' + gen_text
        else:
            yield gen_text

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
import time


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

    logging.debug(f'leading GenerateLyrics')
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
    - Get 20 sentences of length greater than 20.
    - Sleep for 0.5 seconds between sentences (thinking time)


    :param text_input: starting lyric from the input form
    :return: sanitised lyrics for rendering (str)
    """

    start_time = time.time()

    generator = get_generator(weights_path='./model/ckpt_')

    logging.debug('loading character maps')
    generator.load_character_maps(
        character_map_load_path='./model/character_index_map.json',
        index_map_load_path='./model/index_character_map.npy')

    sentences = 0

    while sentences < 16:

        logging.debug(f'Generating line {sentences} at {time.time() - start_time}')

        generated_text = generator.generate_sentence(start_string=text_input,
                                                     temperature=0.87)

        gen_text = CleanOutput.sanitise_string(text_in=generated_text, custom_badwords=custom_badwords)

        if len(gen_text) > 20:
            logging.debug(f'capitalising_first_character')
            gen_text = CleanOutput.clean_sentence(sentence_in=gen_text)

            if sentences > 0:
                time.sleep(0.5)

            sentences += 1

            stop_char = '<br><br>' if sentences % 4 == 0 else '<br>'
            # TODO: this should be debug level when we're happy with it
            logging.info(f'{gen_text} {stop_char} {sentences}')
            yield gen_text + stop_char

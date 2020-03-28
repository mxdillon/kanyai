#!/usr/bin/python
# coding=utf-8
""" Flask server
:usage:
    Routes for KanyAI server - health check and index.
:authors
    JP/CW at 02/01/20
"""
from app.ml.generate_lyrics import GenerateLyrics
from app.ml.clean_output import CleanOutput
from flask import current_app as app
import typing


def get_text(text_input: str, generator: GenerateLyrics) -> typing.Generator:
    """Generate the lyrics for the text input from the model.

    :param text_input: starting lyric from the input form
    :param generator: model generator
    :return: sanitised lyrics for rendering (str)
    """
    if text_input is None:
        return ' '
    else:
        app.logger.info(f'Generating lyrics for {text_input}')

        app.logger.debug(f'ensuring space for {text_input}')
        start_phrase = CleanOutput.ensure_space(text_input)

        app.logger.debug('generating text')
        generated_text = generator.generate_text(start_string=start_phrase,
                                                 num_words=200,
                                                 temperature=0.8)

        return generated_text


def get_generator(model_folder: str, checkpoint_directory: str) -> GenerateLyrics:
    """Instantiate the generator class with a saved model and generate a lyrics string.

    :param model_folder: name of the folder containing the model weights
    :param checkpoint_directory: path to the file containing the model folder
    :return: GenerateLyrics class with the model already loaded
    """

    return GenerateLyrics(model_folder=model_folder, checkpoint_directory=checkpoint_directory)

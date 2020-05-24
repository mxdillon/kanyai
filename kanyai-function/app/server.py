#!/usr/bin/python
# coding=utf-8
"""Application functions.

:usage:
    Routes for kanyAI server - health check and index.
:authors
    JP/MD at 02/01/20
"""

from app.generate_lyrics import GenerateLyrics
from app.clean_output import CleanOutput
from google.cloud import storage

import logging
import os
import zipfile


def get_input(request):
    """Get the input song from the request form."""
    return request.form.get('input')


def get_text(text_input: str, num_words: int, generator: GenerateLyrics) -> str:
    """Generate the lyrics for the text input from the model.

    :param text_input: starting lyric from the input form
    :param num_words: # words to generate
    :param generator: model generator
    :return: sanitised lyrics for rendering (str)get
    """
    if text_input is None:
        return ' '
    else:
        logging.info(f'Generating lyrics for {text_input}')

        logging.debug(f'ensuring space for {text_input}')
        start_phrase = CleanOutput.ensure_space(text_input)

        logging.debug('generating text')
        generated_text = generator.generate_text(start_string=start_phrase,
                                                 num_words=num_words,
                                                 temperature=0.8)

        return generated_text


def unzip_model(tmp_file):
    """Unzip the model to /tmp.

    This is not ideal but:
    - There's a maximum deployment size for GCP Functions
    - Cloud Run (hosted Docker container) is failing, unsure why but the issue is also seen in
    https://minimaxir.com/apps/gpt2-small/
    - App engine is $$$$ expensive
    """
    logging.info(f'unzipping {tmp_file}')

    model_dir = '/tmp'

    with zipfile.ZipFile(tmp_file, 'r') as zip_ref:
        zip_ref.extractall(model_dir)

    logging.info(f'removing {tmp_file} to save on memory')
    os.remove(tmp_file)


def get_model(model_file, tmp_file):
    """Download the model from GCS."""
    storage_client = storage.Client()

    logging.info(f'downloading {model_file} to {tmp_file}')

    storage_client.bucket('model-for-functions') \
        .blob(model_file) \
        .download_to_filename(tmp_file)

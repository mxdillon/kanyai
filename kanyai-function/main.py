#!/usr/bin/python
# coding=utf-8
"""KanyAI application.

:authors
    JP/MD at 02/01/20
"""
from app import server
from app.generate_lyrics import GenerateLyrics
import logging
import google.cloud.logging
from google.cloud.logging.handlers import CloudLoggingHandler, setup_logging

# Configure logging
client = google.cloud.logging.Client()
handler = CloudLoggingHandler(client)
logging.getLogger().setLevel(logging.INFO)
setup_logging(handler)


def get_lyrics(request):
    """Call the KanyAI model and return the generated song."""
    # Set CORS headers for the main request
    headers = {
        # TODO - restrict this to production UI URL / IP range when live
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST',
    }

    model_file = 'model.zip'
    tmp_file = f'/tmp/{model_file}'

    if not server.check_file_exists('/tmp/model/gpt2-simple/model-690.data-00000-of-00001'):

        if not server.check_file_exists(tmp_file):
            server.get_model(model_file, tmp_file)

        server.unzip_model(tmp_file)

    # New gpt_2_simple instance each time,= due to tf 1.x sessions
    generator = GenerateLyrics(model_folder='gpt2-simple', checkpoint_directory='/tmp/model')

    text_input = server.get_input(request)

    clean_text = server.get_text(text_input=text_input, num_words=80, generator=generator)

    return (clean_text, 200, headers)

#!/usr/bin/python
# coding=utf-8
""" KanyAI application
:usage:
    Flask application.
:authors
    JP/CW at 02/01/20
"""

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from better_profanity import profanity
import logging
from src.server import get_text
from src.log_setup import log_config

app = Flask(__name__)
CORS(app)


@app.route('/health', methods=['GET'])
def health():
    """Healthcheck endpoint for application monitoring."""
    logging.debug('healthcheck')
    return jsonify({"Status": 'OK'})


@app.route("/", methods=["GET", "POST"])
def index():
    """Index route for lyric entry and generation.

    POST requests are from submissions.
    GET are the initial rendering of the page (no text input or result).
    """
    logging.debug(f'processing index request {request.method}')
    if request.method == 'POST':
        # Get the input from the from, set it to an single string if empty
        text_input = request.form.get('text_input')
        logging.debug(f'got {text_input} from form')
        text_input = text_input if text_input else ' '

        logging.debug(f'getting clean text')
        clean_text = get_text(text_input)

        return render_template('index.html', text_input=text_input,
                               result=clean_text)

    return render_template('index.html', text_input="", result="")


def create_app():
    """Create the Flask application."""
    profanity.load_censor_words()
    return app


# Configure logger
log_config()
logging.info('starting application')


if __name__ == "__main__":
    # Create and run application
    app = create_app()
    app.run()

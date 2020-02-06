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
from src.server import get_text
from src.ml.generate_lyrics import sanitise_string
from src.config.log_setup import log_config
from src.config.profanity import custom_badwords
import logging

# Create the Flask web application
app = Flask(__name__)
CORS(app)

# Configure logger
log_config()
logging.info('starting application')


@app.route('/health', methods=['GET'])
def health():
    """Healthcheck endpoint for application monitoring."""
    return jsonify({"Status": 'OK'})


@app.route("/", methods=["GET", "POST"])
def index():
    """Index route for lyric entry and generation.

    POST requests are from submissions.
    GET are the initial rendering of the page (no text input or result).
    """

    if request.method == 'POST':
        # Get the input from the form, set it to an single space if empty
        text_input = request.form.get('text_input')
        text_input = text_input if text_input else ' '
        # Generate lyrics and sanitise user input
        clean_text = get_text(text_input)
        clean_input = sanitise_string(text_in=text_input, custom_badwords=custom_badwords)

        return render_template('index.html', text_input=clean_input,
                               result=clean_text)

    return render_template('index.html', text_input="", result="")


def create_app():
    """Create the Flask application."""
    return app


if __name__ == "__main__":
    app = create_app()
    app.run()

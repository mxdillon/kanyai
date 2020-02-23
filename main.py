#!/usr/bin/python
# coding=utf-8
""" KanyAI application
:usage:
    Flask application.
:authors
    JP/CW at 02/01/20
"""

from flask import Flask, jsonify, render_template, request, Response, stream_with_context
from flask_cors import CORS
from app.server import get_text, stream_text
from app.ml.clean_output import CleanOutput
from app.config.log_setup import log_config
from app.config.profanity import custom_badwords
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
        clean_input = CleanOutput.sanitise_string(text_in=text_input, custom_badwords=custom_badwords)

        return render_template('index.html', text_input=clean_input,
                               result=clean_text)

    return render_template('index.html', text_input="", result="")


def stream_template(template_name, **context):
    """Stream a Jinja template as per https://flask.palletsprojects.com/en/1.1.x/patterns/streaming/"""
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    return rv


@app.route("/stream", methods=["GET", "POST"])
def stream():
    """Main streaming route for lyric entry"""

    if request.method == 'POST':
        # Get the input
        text_input = request.form.get('text_input')
        text_input = text_input if text_input else ' '
        clean_input = CleanOutput.sanitise_string(text_in=text_input, custom_badwords=custom_badwords)
        logging.info(f'Streaming song for {clean_input}')

        # Get the generator
        result = stream_text(clean_input)
        return Response(
            stream_template('index-stream.html', text_input=clean_input, result=(stream_with_context(result))))

    return render_template('index-stream.html', text_input="", result="")


def create_app():
    """Create the Flask application."""
    return app


if __name__ == "__main__":
    app = create_app()
    app.run()

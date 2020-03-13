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
from app.server import get_text, get_generator
from app.ml.clean_output import CleanOutput
from app.config.log_setup import log_config
from app.config.profanity import custom_badwords
import logging

# Create the Flask web application
app = Flask(__name__)
CORS(app)

# Configure Gunicorn logger
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

# Configure Flask logger
log_config()
app.logger.info('starting application')

generator = get_generator(weights_path='./model/ckpt_')


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

        clean_text = get_text(text_input, generator)
        clean_input = CleanOutput.sanitise_string(text_in=text_input, custom_badwords=custom_badwords)

        return Response(
            stream_template('index.html', text_input=clean_input, result=(stream_with_context(clean_text))))

    return render_template('index.html', text_input="", result="")


def stream_template(template_name, **context):
    """Stream a Jinja template as per https://flask.palletsprojects.com/en/1.1.x/patterns/streaming/"""
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    return rv


def create_app():
    """Create the Flask application."""
    return app


if __name__ == "__main__":
    app = create_app()
    app.run()

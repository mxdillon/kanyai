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
from better_profanity import profanity

app = Flask(__name__)
CORS(app)


@app.route('/health', methods=['GET'])
def health():
    """Healthcheck endpoint for application monitoring."""
    return jsonify({"Status": 'OK'})


@app.route("/", methods=["GET", "POST"])
def index():
    """Index route for lyric entry and generation.

    POST requests are from submissions.
    GET are the initial rendering of the page.
    """

    if request.method == 'POST':
        # Get the input from the from, set it to an single string if empty
        text_input = request.form.get('text_input')
        text_input = text_input if text_input else ' '

        clean_text = get_text(text_input)

        return render_template('index.html', text_input=text_input,
                               result=clean_text)

    return render_template('index.html', text_input="", result="")


def create_app():
    """Create the Flask application."""
    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
    profanity.load_censor_words()

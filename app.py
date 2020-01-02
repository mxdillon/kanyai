#!/usr/bin/python
# coding=utf-8
""" KanyAI application
:usage:
    Flask application.
:authors
    JP/CW at 02/01/20
"""

from flask import Flask
from flask_cors import CORS
from src.server import health_route, index_route
from better_profanity import profanity

app = Flask(__name__)
CORS(app)


@app.route('/health', methods=['GET'])
def health():
    return health_route()


@app.route("/", methods=["GET", "POST"])
def index():
    return index_route()


def create_app():
    """Create the Flask application."""
    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
    profanity.load_censor_words()

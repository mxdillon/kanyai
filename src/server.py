#!/usr/bin/python
# coding=utf-8
""" Flask server
:usage:
    Routes for KanyAI server - healthc heck and index.
:authors
    JP/CW at 02/01/20
"""

from flask import request, render_template, jsonify
from src.ml.generate_lyrics import call_generator


def health_route():
    return jsonify({"Status": 'OK'})


def index_route():
    if request.method == 'GET':

        text_input = request.args.get('text_input')
        if text_input is None:
            text_input = " "

        else:
            generated_text = call_generator(start_phrase=text_input,
                                            weights_path='./model/1_2la512-256emb512lr003/ckpt_50',
                                            string_length=500)

        return render_template('index.html', text_input=text_input,
                               result=generated_text)

    return render_template('index.html')

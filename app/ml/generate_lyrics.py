#!/usr/bin/python
# coding=utf-8
"""Machine Learning Model
:usage:
    Class to generate lyrics based on a user-defined start phrase and a pretrained model.
:authors
    MD at 20/12/19
"""

import json
import numpy as np
import tensorflow as tf
from flask import current_app as app
import time
from app.ml.clean_output import CleanOutput
from app.config.profanity import custom_badwords

# Tensorflow CPU in Docker perf suggestion from:
# https://www.freecodecamp.org/news/how-a-badly-configured-tensorflow-in-docker-can-be-10x-slower-than-expected-3ac89f33d625/
tf.config.threading.inter_op_parallelism_threads = 1
tf.config.threading.intra_op_parallelism_threads = 1


class GenerateLyrics:
    """Generate lyrics with user defined start string with a saved model."""

    def __init__(self, embedding_dim: int):
        """
        :param embedding_dim: size of vector representation for each character. This MUST match the embedding dimension
        of the saved model that is loaded during generation
        """

        self.embedding_dim = embedding_dim

        self.ind_to_char_map = None
        self.char_to_ind_map = None
        self.vocab_size = None
        self.model = None
        self.generated_str = None

    def load_character_maps(self, character_map_load_path: str, index_map_load_path: str):
        """Load array and dictionary into memory.

        :param character_map_load_path: str containing path of character to index map stored as .json
        :param index_map_load_path: str containing path of index to character map stored as .npy
        :return: None
        """
        self.ind_to_char_map = np.load(index_map_load_path, allow_pickle=True)

        with open(character_map_load_path, 'r') as dictionary:
            self.char_to_ind_map = json.load(dictionary)

        self.vocab_size = self.ind_to_char_map.shape[0]

    def define_model(self, batch_size):
        """Define tensorflow model. Prints model summary to terminal

        :param batch_size: 2^n - indicates the size of batches model will be trained in. Included as parameter here
        as we want to have a batch size of 1 when generating, ie not the same as when training
        :return: None
        """
        self.model = tf.keras.Sequential([
            tf.keras.layers.Embedding(input_dim=self.vocab_size,
                                      output_dim=self.embedding_dim,
                                      batch_input_shape=[batch_size, None]),
            tf.keras.layers.GRU(units=512,
                                activation='sigmoid',
                                return_sequences=True,
                                stateful=True,
                                recurrent_initializer='glorot_uniform'),
            tf.keras.layers.GRU(units=256,
                                activation='sigmoid',
                                return_sequences=True,
                                stateful=True,
                                recurrent_initializer='glorot_uniform'),
            tf.keras.layers.Dense(units=self.vocab_size)
        ])

    def rebuild_model(self, batch_size, weights_path: str):
        """Rebuild model with best weights for text generation.

        :param batch_size: size of batch of examples to be generated. Has only been tested on =1
        :param weights_path: str of path to weights file to use
        :return: None
        """

        self.define_model(batch_size=batch_size)
        self.model.load_weights(weights_path)
        self.model.build(tf.TensorShape([batch_size, None]))

    def generate_text(self, start_string: str, num_characters: int, temperature: float):
        """Generate string starting with start_string of length num_characters using rebuilt model.

        :param start_string: str user wishes to start generation with. Can be a single letter.
        :param num_characters: number of characters you wish to be generated
        :param temperature: parameter that determines how 'surprising' the predictions are. value of 1 is neutral,
        lower is more predictable, higher is more surprising
        :return: string of generated text
        """

        app.logger.debug('converting input')
        input_eval = [self.char_to_ind_map[s] for s in start_string]
        input_eval = tf.expand_dims(input_eval, 0)

        app.logger.debug('resetting model')
        self.model.reset_states()

        self.generated_str = []
        lyric_time = time.time()

        app.logger.debug('looping through characters')
        for _ in range(num_characters):
            app.logger.debug('char loop - loading model - I think')
            predictions = self.model(input_eval)

            app.logger.debug('char loop - squeezing')
            predictions = tf.squeeze(predictions, 0) / temperature

            app.logger.debug('char loop - get an id')
            predicted_id = tf.random.categorical(predictions, num_samples=1)[-1, 0].numpy()

            app.logger.debug('char loop - looping through characters')
            input_eval = tf.expand_dims([predicted_id], 0)

            next_char = self.ind_to_char_map[predicted_id]
            self.generated_str.append(next_char)

            if next_char == '\n':
                txt = ''.join(self.generated_str)
                line = txt.split('\n')[-2] + '<br>'
                line = CleanOutput.capitalise_first_character(text_in=line)
                line = CleanOutput.clean_line(text_in=line)
                line = CleanOutput.sanitise_string(text_in=line, custom_badwords=custom_badwords)

                elapsed_time = time.time() - lyric_time
                app.logger.info(f'{line} at {elapsed_time:.2f}')

                lyric_time = time.time()
                yield line

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
import gpt_2_simple as gpt2
from datetime import datetime
from flask import current_app as app
from app.ml.clean_output import CleanOutput
from app.config.profanity import custom_badwords


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

    def generate_text(self, start_string: str, num_words: int, temperature: float):
        """Generate string starting with start_string of length num_characters using rebuilt model.

        :param start_string: str user wishes to start generation with. Can be a single letter.
        :param num_words: number of words you wish to be generated. Note time to generate increases
        :param temperature: parameter that determines how 'surprising' the predictions are. value of 1 is neutral,
        lower is more predictable, higher is more surprising
        :return: string of generated text
        """

        sess = gpt2.start_tf_sess()
        gpt2.load_gpt2(sess, run_name='run1', checkpoint_dir='gpt')

        gen_start_time = datetime.now()

        txt = gpt2.generate(sess, run_name='run1', checkpoint_dir='gpt', length=num_words, temperature=temperature,
                            prefix=start_string, return_as_list=True)[0]

        time_to_generate = datetime.now() - gen_start_time
        app.logger.debug(f'Time taken to generate lyrics {time_to_generate}')

        txt = txt.split('\n')[-2] + '<br>'
        txt = CleanOutput.capitalise_first_character(text_in=txt)
        txt = CleanOutput.clean_line(text_in=txt)
        txt = CleanOutput.sanitise_string(text_in=txt, custom_badwords=custom_badwords)

        return txt

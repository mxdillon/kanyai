#!/usr/bin/python
# coding=utf-8
""" Machine Learning Model
:usage:
    Class to generate lyrics based on a user-defined start phrase and a pretrained model.
:authors
    MD at 20/12/19
"""

import json
import numpy as np
import tensorflow as tf


class GenerateLyrics:
    """Generate lyrics with user defined start string with a saved model loaded from Google storage."""

    def __init__(self, embedding_dim: int):
        """
        :param embedding_dim: size of vector representation for each character
        """

        self.embedding_dim = embedding_dim

        self.ind_to_char_map = None
        self.char_to_ind_map = None
        self.vocab_size = None

    def load_character_maps(self, character_map_load_path: str, index_map_load_path: str) -> tuple:
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
        :return: tf model
        """
        model = tf.keras.Sequential([
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

        print(model.summary())
        return model

    def rebuild_model(self, batch_size, weights_path: str):
        """Rebuild model with best weights for text generation.

        :param batch_size: size of batch of examples to be generated. Has only been tested on =1
        :param weights_path: str of path to weights file to use
        :return: tf.model
        """

        prediction_model = self.define_model(batch_size=batch_size)
        prediction_model.load_weights(weights_path)
        prediction_model.build(tf.TensorShape([batch_size, None]))
        print(prediction_model.summary())

        return prediction_model

    def generate_text(self, model, start_string: str, num_characters: int, temperature: float):
        """Generate string starting with start_string of length num_characters using rebuilt model.

        :param model: model rebuilt with weights from a training checkpoint
        :param start_string: str user wishes to start generation with. Can be a single letter. May be case sensitive,
        depending on the data used for training
        :param num_characters: number of characters you wish to be generated
        :param self.ind_to_char_map: np.array mapping indices back to characters
        :param temperature: parameter that determines how 'surprising' the predictions are. value of 1 is neutral,
        lower is more predictable, higher is more surprising
        :return: string of generated text
        """

        input_eval = [self.char_to_ind_map[s] for s in start_string]
        input_eval = tf.expand_dims(input_eval, 0)

        generated_str = []

        model.reset_states()
        for i in range(num_characters):
            predictions = model(input_eval)
            predictions = tf.squeeze(predictions, 0) / temperature
            predicted_id = tf.random.categorical(predictions, num_samples=1)[-1, 0].numpy()

            input_eval = tf.expand_dims([predicted_id], 0)

            generated_str.append(self.ind_to_char_map[predicted_id])

        return (start_string + ''.join(generated_str))

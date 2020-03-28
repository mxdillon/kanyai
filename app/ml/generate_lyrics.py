#!/usr/bin/python
# coding=utf-8
"""Machine Learning Model
:usage:
    Class to generate lyrics based on a user-defined start phrase and a pretrained model.
:authors
    MD at 20/12/19
"""

import gpt_2_simple as gpt2
from datetime import datetime
from flask import current_app as app
from app.ml.clean_output import CleanOutput
from app.config.profanity import custom_badwords


class GenerateLyrics:
    """Generate lyrics with user defined start string with a saved gtp2-simple model."""

    def __init__(self, model_folder: str, checkpoint_directory: str):
        """
        :param model_folder: name of the folder containing the model weights
        :param checkpoint_directory: path to the file containing the model folder
        """
        self.model_folder = model_folder
        self.checkpoint_directory = checkpoint_directory

        self.sess = gpt2.start_tf_sess()
        gpt2.load_gpt2(self.sess, run_name=self.model_folder, checkpoint_dir=self.checkpoint_directory)

    def generate_text(self, start_string: str, num_words: int, temperature: float):
        """Generate string starting with start_string of length num_characters using rebuilt model.

        :param start_string: str user wishes to start generation with. Can be a single letter.
        :param num_words: number of words you wish to be generated. Note time to generate increases
        :param temperature: parameter that determines how 'surprising' the predictions are. value of 1 is neutral,
        lower is more predictable, higher is more surprising
        :return: string of generated text
        """

        gen_start_time = datetime.now()

        txt = \
            gpt2.generate(self.sess, run_name=self.model_folder, checkpoint_dir=self.checkpoint_directory,
                          length=num_words, temperature=temperature, prefix=start_string, return_as_list=True)[0]

        time_to_generate = datetime.now() - gen_start_time
        app.logger.debug(f'Time taken to generate lyrics {time_to_generate}')

        txt = txt.split('\n')[-2] + '<br>'
        txt = CleanOutput.capitalise_first_character(text_in=txt)
        txt = CleanOutput.clean_line(text_in=txt)
        txt = CleanOutput.sanitise_string(text_in=txt, custom_badwords=custom_badwords)

        return txt

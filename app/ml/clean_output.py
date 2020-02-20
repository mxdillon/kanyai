#!/usr/bin/python
# coding=utf-8
"""Machine Learning Output Cleaning
:usage:
    Class to clean generated lyrics.
:authors
    MD at 20/02/20
"""

import re


class CleanOutput:
    """Format output strings so they can be presented to user."""

    @staticmethod
    def sanitise_string(text_in: str, custom_badwords: list) -> str:
        """Clean an input string of all swear words. Replace them with '****'.

        :param custom_badwords: list of custom swearwords
        :param text_in: string containing text to be sanitised
        :return: string of sanitised text
        """
        for word in custom_badwords:
            text_in = re.sub(word, '****', text_in, flags=re.I)
        return text_in

    @staticmethod
    def capitalise_first_character(text_in: str) -> str:
        """Capitalise the first character in the generated lyrics. If first character is a space, remove it and capitalise.

        :param text_in: string of generated lyrics
        :return: string with capital at the start
        """
        if text_in[0] == ' ':
            text_rtn = text_in[1:]
        else:
            text_rtn = text_in
        return text_rtn[0].upper() + text_rtn[1:]

    @staticmethod
    def ensure_space(text_in: str) -> str:
        """Ensure there is a space at the end of the user input so that lyric generation starts by generating a new word.

        :param text_in: text input from user
        :return: text input from user, ensuring there is a space at the end
        """
        if text_in[-1] == ' ':
            return text_in
        else:
            return text_in + ' '

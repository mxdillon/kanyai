#!/usr/bin/python
# coding=utf-8
"""Performance profiling of the application by consuming debug logs.
:usage:
    Run ad hoc.
:authors
    JP at 05/01/20
"""
from src.config.log_setup import log_config
from src.server import get_text
import logging
import time
import pandas as pd


class ListHandler(logging.Handler):
    """A safe logging.Handler that writes messages into a list."""

    def __init__(self, log_list):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Our custom argument
        self.log_list = log_list

    def emit(self, record):
        # record.message is the log message
        self.log_list.append([time.time(), record.msg, record.levelname, record.funcName, record.lineno])


def configure_logging():
    """Configure the logger, add a custom logger to a list.

    :return: log_list - list of
    """
    # Instantiate logging and add list handler
    log_config(google_logger=False)

    # Get the logger, add the list handler
    logger = logging.getLogger()
    log_list = []
    list_handler = ListHandler(log_list)
    logger.addHandler(list_handler)

    # Log at debug level as that's where the interesting messages are
    logger.setLevel(logging.DEBUG)
    return log_list


def get_term_logs_to_df():
    """ Call get_text to generate lyrics, store the logs in a DataFrame

    :return: DataFrame of logs for the get_text method
    """
    dfs = []

    # For each test term, configure the logger and call the main function
    for term in test_terms:
        configured_log_list = configure_logging()
        get_text(term)

        # Convert log list to a DataFrame for
        df_term = pd.DataFrame(configured_log_list)
        df_term['term'] = term
        df_term.columns = ['time', 'msg', 'levelname', 'funcName', 'lineno', 'term']
        dfs.append(df_term)

    return pd.concat(dfs)


test_terms = ['james', ' ']  # , 'a song about logging', 'the messiah']

if __name__ == '__main__':
    df = get_term_logs_to_df()

    # Get the time of the next log entry and compare
    df['time_lead'] = df.groupby(['term'])['time'].shift(-1)
    df['time_elapsed'] = df['time_lead'] - df['time']

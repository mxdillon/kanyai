#!/usr/bin/python
# coding=utf-8
""" Log setup for application including Google Cloud logging.
:usage:
    Setup logs during app creation.
:authors
    JP at 05/01/20
"""
import google.cloud.logging
import logging


def log_config(google_logger=True):
    """Instantiate Google Cloud logging and format logger.

    :param google_logger: boolean to set up Google Cloud logging or not
    """

    if google_logger:
        # Create client for Google Cloud StackDriver logging
        client = google.cloud.logging.Client()
        client.setup_logging()
    # # Add a stream handler to print to stdout
    log = logging.getLogger()

    # Format loggers
    for handler in log.handlers:
        handler.level = logging.INFO

#!/usr/bin/python
# coding=utf-8
""" Log setup for application.
:usage:
    Setup logs during app creation.
:authors
    JP at 05/01/20
"""
import logging


def log_config():
    """Instantiate logging and format logger."""
    # # Add a stream handler to print to stdout
    log = logging.getLogger()

    # Format loggers
    for handler in log.handlers:
        handler.level = logging.INFO

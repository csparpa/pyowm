#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging


def get_default_logger():
    """
    Returns a basic Python std out logger

    :returns: a `logging.Logger` instance
    """
    logging.basicConfig(
        level=logging.WARNING,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S%z'
    )
    logger = logging.getLogger('pyowm')
    logger.level = logging.WARNING
    return logger

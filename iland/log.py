# -*- coding: utf-8 -*-

"""A library that provides a custom logger for the `iland.Api` object."""

import logging
import sys

#: A custom Python logging logger for the `iland.Api` object.
LOG = logging.getLogger('iland_sdk')
LOG.setLevel(logging.INFO)

ch = logging.StreamHandler(sys.__stdout__)
ch.setLevel(logging.INFO)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

LOG.addHandler(ch)

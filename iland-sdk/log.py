# -*- coding: utf-8 -*-

import logging
import sys

LOG = logging.getLogger('iland_sdk')
LOG.setLevel(logging.INFO)

ch = logging.StreamHandler(sys.__stdout__)
ch.setLevel(logging.INFO)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

LOG.addHandler(ch)

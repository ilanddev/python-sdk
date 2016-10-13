# -*- coding: utf-8 -*-

"""A module that provides a Python interface to the iland cloud API."""

from .api import Api  # noqa
from .constant import ACCESS_URL  # noqa
from .constant import BASE_URL  # noqa
from .constant import REFRESH_URL  # noqa
from .exception import ApiException  # noqa
from .exception import UnauthorizedException  # noqa

__author__ = 'iland Internet Solutions, Corp'
__email__ = 'devops@iland.com'
__version__ = '0.7.0'

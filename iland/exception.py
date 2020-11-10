# -*- coding: utf-8 -*-

"""A library that provides custom exceptions for the `iland.Api` module."""


class ApiException(Exception):
    """Base class for `iland.Api` errors."""

    @property
    def error(self):
        """Returns the first argument used to construct this error."""
        return self.args[0].get('type')

    @property
    def message(self):
        """Returns the second argument used to construct this error."""
        return self.args[0].get('message')

    @property
    def detail_message(self):
        """Returns the third argument used to construct this error."""
        return self.args[0].get('detail_message')


class UnauthorizedException(ApiException):
    """ Unauthorized `iland.Api` exception. """

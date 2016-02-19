# -*- coding: utf-8 -*-

"""A library that provides custom excptions for the `iland.Api` module."""


class ApiException(Exception):
    """Base class for `iland.Api` errors."""

    @property
    def error(self):
        """Returns the first argument used to construct this error."""
        return self.args[0]

    @property
    def message(self):
        """Returns the second argument used to construct this error."""
        return self.args[1]

    @property
    def detail_message(self):
        """Returns the third argument used to construct this error."""
        return self.args[2]


class UnauthorizedException(ApiException):
    """ Unauthorized `iland.Api` exception. """

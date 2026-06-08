# -*- coding: utf-8 -*-
# bfsi_tools/exceptions.py — all custom exceptions live here


class CircularParseError(Exception):
    """Raised when a circular JSON payload cannot be parsed."""
    pass


class InvalidTierError(Exception):
    """Raised when an unrecognised tier value is encountered."""
    pass


class MissingFieldError(Exception):
    """Raised when a required field is absent from the payload."""
    pass
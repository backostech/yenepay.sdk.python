"""
YenePay exceptions
"""


class CheckoutError(Exception):
    """Exception for checkout errors."""


class PDTError(Exception):
    """Exception for PDT errors."""


class IPNError(Exception):
    """Exception for IPN errors."""

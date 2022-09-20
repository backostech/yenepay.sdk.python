"""
YenePay Python API Representation
"""

from yenepay.constants import (
    CHECKOUT_PRODUCTION_URL,
    CHECKOUT_SANDBOX_URL,
    IPN_PRODUCTION_URL,
    IPN_SANDBOX_URL,
    PDT_PRODUCTION_URL,
    PDT_SANDBOX_URL,
)


class Api:
    """
    A class that represents YenePay API.
    """

    class checkout:
        production = CHECKOUT_PRODUCTION_URL
        sandbox = CHECKOUT_SANDBOX_URL

    class pdt:
        production = PDT_PRODUCTION_URL
        sandbox = PDT_SANDBOX_URL

    class ipn:
        production = IPN_PRODUCTION_URL
        sandbox = IPN_SANDBOX_URL


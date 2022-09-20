"""
YenePay Python API Representation
"""

import typing

import requests

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


class ApiRequest:
    """A class that represents YenePay API request."""

    headers = {"Content-Type": "application/json"}

    @classmethod
    def checkout(
        cls,
        checkout,
        is_sandbox: typing.Optional[bool] = False,
    ) -> typing.Tuple[int, dict]:
        """Make request to checkout url"""

        response = requests.post(
            Api.checkout.sandbox
            if checkout.is_sandbox
            else Api.checkout.production,
            json=checkout.to_dict(),
            headers=cls.headers,
        )
        return response.status_code, response.json()

    @classmethod
    def pdt(
        cls,
        json: typing.Union[str, int, float],
        is_sandbox: typing.Optional[bool] = False,
    ) -> typing.Tuple[int, dict]:
        """Make request to pdt url"""

        response = requests.post(
            Api.pdt.sandbox if is_sandbox else Api.pdt.production,
            json=json,
            headers=cls.headers,
        )
        return response.status_code, response.json()

    @classmethod
    def ipn(
        cls,
        json: typing.Union[str, int, float],
        is_sandbox: typing.Optional[bool] = False,
    ) -> typing.Tuple[int, dict]:
        """Make request to ipn url"""

        response = requests.post(
            Api.ipn.sandbox if is_sandbox else Api.ipn.production,
            json=json,
            headers=cls.headers,
        )
        return response.status_code, response.json()

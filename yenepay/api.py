"""
YenePay Python API Representation
"""
import json
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
        data,
        is_sandbox: typing.Optional[bool] = False,
    ) -> typing.Tuple[int, dict]:
        """Make request to checkout url"""

        response = requests.post(
            Api.checkout.sandbox if is_sandbox else Api.checkout.production,
            json=data,
            headers=cls.headers,
        )
        try:
            return response.status_code, response.json()
        except json.JSONDecodeError:
            content = response.content
            return response.status_code, content

    @classmethod
    def pdt(
        cls,
        data: typing.Union[str, int, float],
        is_sandbox: typing.Optional[bool] = False,
    ) -> typing.Tuple[int, dict]:
        """Make request to pdt url"""

        response = requests.post(
            Api.pdt.sandbox if is_sandbox else Api.pdt.production,
            json=data,
            headers=cls.headers,
        )
        try:
            return response.status_code, response.json()
        except json.JSONDecodeError:
            content = response.content
            return response.status_code, content

    @classmethod
    def ipn(
        cls,
        data: typing.Union[str, int, float],
        is_sandbox: typing.Optional[bool] = False,
    ) -> typing.Tuple[int, dict]:
        """Make request to ipn url"""

        response = requests.post(
            Api.ipn.sandbox if is_sandbox else Api.ipn.production,
            data=json,
            headers=cls.headers,
        )
        return response.status_code, response.json()

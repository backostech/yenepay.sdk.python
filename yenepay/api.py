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
        """Checkout endpoints."""

        production = CHECKOUT_PRODUCTION_URL
        sandbox = CHECKOUT_SANDBOX_URL

    class pdt:
        """PDT endpoints."""

        production = PDT_PRODUCTION_URL
        sandbox = PDT_SANDBOX_URL

    class ipn:
        """IPN endpoints."""

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
        """
        Send request to yenepay checkout endpoint.

        :param data: parameters that needed to be sent to YenePay server.
        :type data: :func:`dict`

        :param is_sandbox: Whether the given client account is usng sandbox
                environment or not.
        :type is_sandbox: :func:`bool`

        :returns: Request respose status and content.
        :rtype: Tuple of :func:`int` and :func:`bytes` or :func:`json`
        """

        response = requests.post(
            Api.checkout.sandbox if is_sandbox else Api.checkout.production,
            json=data,
            headers=cls.headers,
        )
        try:
            return response.status_code, response.json()
        except json.JSONDecodeError:
            return response.status_code, response.content

    @classmethod
    def pdt(
        cls,
        data: typing.Union[str, int, float],
        is_sandbox: typing.Optional[bool] = False,
    ) -> typing.Tuple[int, dict]:
        """
        Send request to yenepay PDT endpoint.

        :param data: parameters that needed to be sent to YenePay server.
        :type data: :func:`dict`

        :param is_sandbox: Whether the given client account is usng sandbox
                environment or not.
        :type is_sandbox: :func:`bool`

        :returns: Request respose status and content.
        :rtype: Tuple of :func:`int` and :func:`bytes` or :func:`json`
        """

        response = requests.post(
            Api.pdt.sandbox if is_sandbox else Api.pdt.production,
            json=data,
            headers=cls.headers,
        )
        try:
            return response.status_code, response.json()
        except json.JSONDecodeError:
            return response.status_code, response.content

    @classmethod
    def ipn(
        cls,
        data: typing.Union[str, int, float],
        is_sandbox: typing.Optional[bool] = False,
    ) -> typing.Tuple[int, dict]:
        """
        Send request to yenepay IPN endpoint.

        :param data: parameters that needed to be sent to YenePay server.
        :type data: :func:`dict`

        :param is_sandbox: Whether the given client account is usng sandbox
                environment or not.
        :type is_sandbox: :func:`bool`

        :returns: Request respose status and content.
        :rtype: Tuple of :func:`int` and :func:`bytes` or :func:`json`
        """

        response = requests.post(
            Api.ipn.sandbox if is_sandbox else Api.ipn.production,
            json=data,
            headers=cls.headers,
        )
        try:
            return response.status_code, response.json()
        except json.JSONDecodeError:
            return response.status_code, response.content

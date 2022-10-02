"""
YenePay PDT model.
"""

import re
from pprint import pformat

from requests import codes

from yenepay.api import ApiRequest
from yenepay.exceptions import PDTError
from yenepay.helpers import Validator, to_python_attr


class PDT(Validator):
    """A class to checks the latest status of a payment order"""

    def __init__(
        self,
        client,
        merchant_order_id: str,
        transaction_id: str,
        use_sandbox=False,
    ) -> None:
        """
        :param client: yenepay client account
        :type client: :class:`yenepay.models.client.Client`

        :param transaction_id: a unique identifier id of the payment
                transaction that is set on YenePay’s platform. This id can
                be obtained from your SuccessUrl or IPNUrl endpoints.
        :type transaction_id: :func:`str`

        :param merchant_order_id: the order id for this transaction that is
                set on your platform.
        :type merchant_order_id: :func:`str`

        :param use_sandbox: Use sandbox environment. Default is False.
        :type use_sandbox: Optional :func:`bool`

        :rtype: :obj:`None`
        """

        self._client = client
        self.merchantOrderId = merchant_order_id
        self.transactionId = transaction_id
        self.use_sandbox = use_sandbox

    def _validate_client(self, value):
        """validate client attribute."""
        from yenepay.models.client import Client

        if not isinstance(value, Client):
            raise TypeError(
                "client attribute must be instance of yenepay.Client, got "
                "{}".format(type(self._client).__name__)
            )

    @property
    def requestType(self) -> str:
        """
        :return: PDT request type. always `PDT`
        :rtype: :func:`str`
        """
        return "PDT"

    @property
    def request_type(self) -> str:
        """
        :return: PDT request type. alway `PDT`
        :rtype: :func:`str`
        """
        return self.requestType

    @property
    def token(self) -> str:
        """
        :return: client pdt token.
        :rtype: :func:`str`
        """
        return self._client.pdtToken

    @property
    def pdtToken(self) -> str:
        """
        :return: client pdt token.
        :rtype: :func:`str`
        """
        return self._client.pdtToken

    @property
    def transaction_id(self) -> str:
        """
        :return: checkout transaction id.
        :rtype: :func:`str`
        """
        return self.transactionId

    @transaction_id.setter
    def transaction_id(self, value: str) -> None:
        """set transaction id."""
        self.transactionId = value

    @property
    def merchant_order_id(self) -> str:
        """
        :return: checkout merchant order id.
        :rtype: :func:`str`
        """
        return self.merchantOrderId

    @merchant_order_id.setter
    def merchant_order_id(self, value: str) -> None:
        """set merchant order id."""
        self.merchantOrderId = value

    @property
    def is_sandbox(self) -> bool:
        """
        check client running sandbox environment.

        :rtype: :func:`bool`
        """
        return self.use_sandbox

    @is_sandbox.setter
    def is_sandbox(self, value: bool) -> None:
        """set PDT sandbox status"""
        self.use_sandbox = value

    def to_dict(self) -> dict:
        """
        Convert PDT properties into dictionary object.

        :return: dictionary of PDT properties
        :rtype: :func:`dict`
        """
        return {
            "requestType": self.requestType,
            "pdtToken": self.pdtToken,
            "transactionId": self.transactionId,
            "merchantOrderId": self.merchantOrderId,
        }

    def check_status(self):
        """
        Check the latest status of a given payment order.

        :return: PDT Status
        :rtype: :class:`yenepay.models.pdt.PDTResponse`
        """

        status_code, response = ApiRequest.pdt(self.to_dict(), self.is_sandbox)
        if status_code == codes.ok:
            return PDTResponse(response, self)
        else:
            raise PDTError(pformat(response))

    def __repr__(self) -> str:
        """return pdt representation."""
        return "<PDT {}>".format(self.pdtToken)

    def __str__(self) -> str:
        """return pdt string representation."""
        return self.__repr__()


class PDTResponse:
    """PDT status resposen class."""

    def __init__(self, response: str, pdt: PDT) -> None:
        """
        :param response: Actutal response from api endpoint.
        :type response: :func:`str`

        :param pdt: a PDT instance that reqest in sent from.
        :type pdt: :class:`yenepay.models.pdt.PDT`

        :rtype: :obj:`None`
        """

        self._response = response
        self.pdt = pdt

        pattern = r"(?:(\w+)=(\w+))"
        matches = re.findall(pattern, self._response)

        for attr, value in matches:
            setattr(self, to_python_attr(attr), value)

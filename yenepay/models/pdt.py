"""
YenePay PDT model.
"""

import re
from pprint import pformat

from requests import codes

from yenepay.api import ApiRequest
from yenepay.exceptions import CheckoutError


class PDT:
    """PDT model."""

    def __init__(
        self,
        client,
        merchant_order_id: str,
        transaction_id: str,
        use_sandbox=False,
    ) -> None:
        """Checks the latest status of a payment order

        :params client: yenepay.Client instance.
        :params transaction_id: a unique identifier id of the payment
                    transaction that is set on YenePay’s platform. This id can
                    be obtained from your SuccessUrl or IPNUrl endpoints.
        :params merchant_order_id: the order id for this transaction that is
                    set on your platform.
        """

        self._client = client
        self.merchantOrderId = merchant_order_id
        self.transactionId = transaction_id
        self.use_sandbox = use_sandbox

    @property
    def requestType(self) -> str:
        """return request type."""
        return "PDT"

    @property
    def request_type(self) -> str:
        """return request typel."""
        return self.requestType

    @property
    def token(self) -> str:
        """return pdt token."""
        return self._client.pdtToken

    @property
    def pdtToken(self) -> str:
        """return client pdt token."""
        return self._client.pdtToken

    @property
    def transaction_id(self) -> str:
        """return transaction id."""
        return self.transactionId

    @transaction_id.setter
    def transaction_id(self, value: str) -> None:
        """set transaction id."""
        self.transactionId = value

    @property
    def merchant_order_id(self) -> str:
        """return merchant order id."""
        return self.merchantOrderId

    @merchant_order_id.setter
    def merchant_order_id(self, value: str) -> None:
        """set merchant order id."""
        self.merchantOrderId = value

    @property
    def is_sandbox(self) -> bool:
        """check whether the request under sandbox."""
        return self.use_sandbox

    def to_dict(self) -> dict:
        """return dictionary of a PDT."""
        return {
            "requestType": self.requestType,
            "pdtToken": self.pdtToken,
            "transactionId": self.transactionId,
            "merchantOrderId": self.merchantOrderId,
        }

    def check_status(self):
        """check a status of pdt."""

        status_code, response = ApiRequest.pdt(self.to_dict(), self.is_sandbox)
        if status_code == codes.ok:
            return PDTResponse(response, self)
        else:
            raise CheckoutError(pformat(response))

    def __repr__(self) -> str:
        """return pdt representation."""
        return "<PDT {}>".format(self.pdtToken)

    def __str__(self) -> str:
        """return pdt string representation."""
        return self.__repr__()


class PDTResponse:
    """PDT status resposen class."""

    def __init__(self, response: str, pdt: PDT) -> None:
        """PDT status response

        :param response: Actutal response from api endpoint.
        :param pdt: PDT instance

        >>> response = "Status=success&BuyerID=123"
        >>> pdt_response = PDTResponse(response, PDT)
        >>> pdt_response._response == response
        True

        >>> pdt_response.pdt == PDT
        True

        >>> pdt_response.status == "success"
        True

        >>> pdt_response.buyer_id == "123"
        True
        """

        self._response = response
        self.pdt = pdt

        pattern = r"(?:(\w+)=(\w+))"
        matches = re.findall(pattern, self._response)

        for attr, value in matches:
            setattr(self, self._to_python_attr(attr), value)

    def _to_python_attr(self, attr: str) -> str:
        """return a given attribute name into snake case.

        >>> response = PDTResponse("status=success", None)
        >>> response._to_python_attr("TotalAmount")
        'total_amount'

        >>> response._to_python_attr("Status")
        'status'

        >>> response._to_python_attr("BuyerID")
        'buyer_id'
        """
        pattern = r"(?:[A-Z])[a-z0-9_]*"
        attr = attr.replace("ID", "Id")
        matches = re.findall(pattern, attr)

        return "_".join((match.lower() for match in matches))

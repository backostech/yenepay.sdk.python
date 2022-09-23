"""
YenePay API Client model.
"""

import typing

from yenepay.models.checkout import CartCheckout, ExpressCheckout
from yenepay.models.pdt import PDT


class Client:
    """Client model."""

    def __init__(
        self, merchant_id: str, token: typing.Optional[str] = None
    ) -> None:
        """Representation of API client.

        :param merchant_id: A unique merchant short code that is assigned to
                a merchant when signing up for a YenePay merchant account.
                Has a minimum of 4 digits and can be found after signing
                into YenePay account manager (https://www.yenepay.com/account)
        :param token: A request authentication token that is assigned to a
                YenePay merchant account can be found on the Settings page
                of YenePay’s account manager.
        """

        self.merchantId = merchant_id
        self.pdtToken = token

    @property
    def merchant_id(self) -> str:
        """return merchant id."""
        return self.merchantId

    @merchant_id.setter
    def merchant_id(self, value: str) -> None:
        """set merchant id."""
        self.merchantId = value

    @property
    def token(self) -> str:
        """return pdt token."""
        return self.pdtToken

    @token.setter
    def token(self, value: str) -> None:
        """set token."""
        self.pdtToken = value

    def get_cart_checkout(self, *args, **kwargs):
        """return cart checkout."""
        kwargs["client"] = self
        return CartCheckout(*args, **kwargs)

    def get_express_checkout(self, *args, **kwargs):
        """return express checkout."""
        if not isinstance(kwargs.get("items"), (tuple, set, list)):
            kwargs["items"] = [kwargs.get("items")]

        kwargs["client"] = self
        return ExpressCheckout(*args, **kwargs)

    def check_pdt_status(
        self, merchant_order_id: str, transaction_id, use_sandbox: bool = False
    ):
        """check current pdt status."""

        pdt = PDT(
            self, merchant_order_id, transaction_id, use_sandbox=use_sandbox
        )
        return pdt.check_status()

    def __repr__(self) -> str:
        """return representation of client."""
        return "<Client {} - {}>".format(self.merchantId, self.pdtToken)

    def __str__(self) -> str:
        """return string representation of client."""
        return self.__repr__()

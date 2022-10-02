"""
YenePay API Client model.
"""

import typing

from yenepay.models.checkout import CartCheckout, ExpressCheckout
from yenepay.models.pdt import PDT


class Client:
    """Representation of a single merchant account in YenePay platform."""

    def __init__(
        self,
        merchant_id: str,
        token: typing.Optional[str] = None,
        use_sandbox: typing.Optional[bool] = False,
    ) -> None:
        """
        :param merchant_id: A unique merchant short code that is assigned to
                a merchant when signing up for a YenePay merchant account.
                Has a minimum of 4 digits and can be found after signing
                into YenePay account manager (https://www.yenepay.com/account)
        :type merchant_id: :func:`str`

        :param token: A request authentication token that is assigned to a
                YenePay merchant account can be found on the Settings page
                of YenePay’s account manager.
        :type token: :func:`str`

        :param use_sandbox: Use sandbox environment. Default is False.
        :type use_sandbox: Optional :func:`bool`

        :rtype: :obj:`None`
        """

        self.merchantId = merchant_id
        self.pdtToken = token
        self.use_sandbox = use_sandbox

    @property
    def merchant_id(self) -> str:
        """
        :return: client merchant id.
        :rtype: :func:`str`
        """
        return self.merchantId

    @merchant_id.setter
    def merchant_id(self, value: str) -> None:
        """set merchant id."""
        self.merchantId = value

    @property
    def token(self) -> str:
        """
        :return: client pdt token.
        :rtype: :func:`str`
        """
        return self.pdtToken

    @token.setter
    def token(self, value: str) -> None:
        """set token."""
        self.pdtToken = value

    @property
    def is_sandbox(self) -> bool:
        """
        check client running sandbox environment.

        :rtype: :func:`bool`
        """
        return self.use_sandbox

    @is_sandbox.setter
    def is_sandbox(self, value: bool) -> None:
        """set client sandbox status"""
        self.use_sandbox = value

    def get_cart_checkout(self, *args, **kwargs):
        """
        Create :class:`yenepay.models.checkout.CartCheckout` instance
        using a given information. for parameter information refer to
        a class parameters.

        :return: checkout instance
        :rtype: :class:`yenepay.models.checkout.CartCheckout`
        """
        kwargs["client"] = self
        return CartCheckout(*args, **kwargs)

    def get_express_checkout(self, *args, **kwargs):
        """
        Create :class:`yenepay.models.checkout.ExpressCheckout` instance
        using a given information. for parameter information refer to
        a class parameters.

        :return: checkout instance
        :rtype: :class:`yenepay.models.checkout.CartCheckout`
        """
        if not isinstance(kwargs.get("items"), (tuple, set, list)):
            kwargs["items"] = [kwargs.get("items")]

        kwargs["client"] = self
        return ExpressCheckout(*args, **kwargs)

    def check_pdt_status(
        self,
        merchant_order_id: str,
        transaction_id: str,
        use_sandbox: bool = False,
    ):
        """
        Check payment order status for a given transaction.

        :param merchant_order_id: A unique identifier for this payment order
                on the merchant’s platform. Will be used to track payment
                status for this order.
        :type merchant_order_id: Optional :func:`str`

        :param transaction_id: a unique identifier id of the payment
                transaction that is set on YenePay’s platform. This id can be
                obtained from your checkout success_url or ipn_url endpoints.
        :type transaction_id: :func:`str`

        :return: Return pdt respose of a server
        :rtype: :class:`yenepay.models.pdt.PDTRespose`
        :raise yenepay.exceptions.CheckoutError: if paramenters are
                    incorrect.
        """

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

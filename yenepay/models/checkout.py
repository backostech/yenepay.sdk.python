"""
YenePay models
"""
import json
import os
import typing
import uuid
from abc import ABCMeta, abstractmethod
from pprint import pformat

from requests import codes

from yenepay.api import ApiRequest
from yenepay.constants import CART, EXPRESS
from yenepay.exceptions import CheckoutError
from yenepay.models.pdt import PDT


class Item:
    """
    Represent a single item to be purchased.
    """

    def __init__(
        self,
        name: str,
        unit_price: float,
        quantity: int,
        item_id: typing.Optional[str] = None,
    ) -> None:
        """
        Initialize the item.

        :param name: A unique identifier of the item (SKU, UUID,…)
                    that is used to identify the item on the merchant’s
                    platform.
        :param unit_price: Amount in ETB currency. Required for Express type
                    checkout.
        :param quantity: Quantity of the item. Required for Express type
                    checkout.
        :param item_id: Optional item id. Required for Express type
                    checkout.
        """

        self.itemId = item_id or str(uuid.uuid4())
        self.itemName = name
        self.unitPrice = unit_price
        self.quantity = quantity

    @property
    def id(self) -> typing.Union[str, uuid.UUID]:
        """The id property."""
        return self.itemId

    @id.setter
    def id(self, value: str):
        """set item id"""
        self.itemId = value

    @property
    def name(self) -> str:
        """return item name"""
        return self.itemName

    @name.setter
    def name(self, value: str):
        """set item name"""
        self.itemName = value

    @property
    def unit_price(self) -> float:
        """return item unit price."""
        return self.unitPrice

    @unit_price.setter
    def unit_price(self, value: float):
        """set item unit price"""
        self.unitPrice = value

    def to_dict(self) -> dict:
        """return item to dict"""
        return {
            attr: getattr(self, attr, None)
            for attr in ["itemId", "itemName", "unitPrice", "quantity"]
            if getattr(self, attr, None) is not None
        }

    def __repr__(self) -> str:
        """Item representation."""
        return "<Item '{}'>".format(self.name)

    def __str__(self) -> str:
        """return item string represenation."""
        return self.__repr__()


class Checkout(metaclass=ABCMeta):
    """Create YenePay checkout"""

    @abstractmethod
    def __init__(
        self,
        process: str,
        client: str,
        items: typing.List[Item] = [],
        merchant_order_id: typing.Optional[str] = None,
        success_url: typing.Optional[str] = None,
        cancel_url: typing.Optional[str] = None,
        ipn_url: typing.Optional[str] = None,
        failure_url: typing.Optional[str] = None,
        expires_after: typing.Optional[int] = None,
        expires_in_days: typing.Optional[int] = 1,
        total_items_handling_fee: typing.Optional[float] = None,
        total_items_delivery_fee: typing.Optional[float] = None,
        total_items_discount: typing.Optional[float] = None,
        total_items_tax1: typing.Optional[float] = None,
        total_items_tax2: typing.Optional[float] = None,
        use_sandbox: typing.Optional[bool] = False,
    ) -> None:
        """YenePay checkout option

        :param process:  Checkout type for this payment. Should have a value
                    of either Express or Cart. Use Express checkout type for
                    single item payment and Cart if this payment includes more
                    than one item.
        :params client: yenepay.Client instance.
        :param items: Items to be purchased.
        :param merchant_order_id: A unique identifier for this payment order
                    on the merchant’s platform. Will be used to track payment
                    status for this order.
        :param success_url: A fully qualified URL endpoint on the merchant’s
                    platform that will be used to redirect the paying customer
                    after the payment has successfully been completed.
        :param cancel_url: A fully qualified URL endpoint on the merchant’s
                    platform that will be used to redirect the paying
                    customer if this payment is cancelled by the customer.
        :param ipn_url: A fully qualified URL endpoint on the merchant’s
                    platform that will be used to send Instant Payment
                    Notification to the merchant’s platform when a payment
                    is successfully completed.
        :param failure_url: A fully qualified URL endpoint on the merchant’s
                    platform that will be used to redirect the paying customer
                    if this payment fails.
        :param expires_after: Expiration period for this payment in minutes.
                    This payment order will expire after the specified number
                    of minutes, if specified.
        :param expires_in_days: Expiration period for this payment in days.
                    This payment order will expire after the specified number
                    of days. The default value is 1 day.
        :param total_items_handling_fee: Handling fee in ETB currency for this
                    payment order, if applicable. Set this value for Cart type
                    checkout. When calculating total payment amount, this will
                    be added to the cart items total amount.
        :param total_items_delivery_fee: Delivery or shipping fee in ETB
                    currency for this payment order, if applicable. Set this
                    value for Cart type checkout. When calculating total
                    payment amount, this will be added to the cart items total
                    amount.
        :param total_items_discount: Discount amount in ETB currency for this
                    payment order, if applicable. Set this value for Cart type
                    checkout. When calculating total payment amount, this will
                    be deducted from the cart items total amount.
        :param total_items_tax1: Tax amount in ETB currency for this payment
                    order, if applicable. Set this value for Cart type
                    checkout. When calculating total payment amount, this will
                    be added to the cart items total amount.
        :param total_items_tax2: Tax amount in ETB currency for this payment
                    order, if applicable. Set this value for Cart type
                    checkout. When calculating total payment amount, this will
                    be added to the cart items total amount.
        :param use_sandbox: Use sandbox environment. Default is False.
        """

        self._process = process
        self._client = client
        self.items = items
        self.merchantOrderId = merchant_order_id
        self.successUrl = success_url
        self.cancelUrl = cancel_url
        self.ipnUrl = ipn_url
        self.failureUrl = failure_url
        self.expiresAfter = expires_after
        self.expiresInDays = expires_in_days
        self.totalItemsHandlingFee = total_items_handling_fee
        self.totalItemsDeliveryFee = total_items_delivery_fee
        self.totalItemsDiscount = total_items_discount
        self.totalItemsTax1 = total_items_tax1
        self.totalItemsTax2 = total_items_tax2
        self.use_sandbox = (
            use_sandbox or os.environ.get("YENEPAY_ENVIRONMENT") or False
        )
        self._validate()

    def _validate(self) -> None:
        """
        validate configuration.
        """

        if self.process is None:
            raise ValueError("Checkout process cannot be None.")

        if self.process not in (EXPRESS, CART):
            raise ValueError(
                "Process must be {} or {}, got {}".format(
                    EXPRESS, CART, self.process
                )
            )

        if not isinstance(self.items, (tuple, set, list)):
            raise TypeError(
                "Items must be tuple, set or list {}".format(
                    type(self.items).__name__
                )
            )

        if not self.items:
            raise ValueError("Items cannot be empty")

        for idx, item in enumerate(self.items):
            if not isinstance(item, Item):
                raise TypeError(
                    "Checkout item must be type of yenepay.checkout.Item, "
                    "got {} at inde {}".format(type(item).__name__, idx)
                )

        if self.process == EXPRESS and len(self.items) > 1:
            raise ValueError(
                "'{}' process is for a single item. if you want to "
                "purchase multiple item use '{}' for process"
                " parameter.".format(EXPRESS, CART)
            )

    @property
    def process(self) -> str:
        """return checkout process type."""
        return getattr(self, "_process", None)

    @property
    def merchant_id(self) -> str:
        """return merchant id."""
        return self._client.merchantId

    @property
    def merchantId(self) -> str:
        """return merchant id."""
        return self._client.merchantId

    @property
    def token(self) -> str:
        """return client pdt token."""
        return self._client.pdtToken

    @property
    def merchant_order_id(self) -> typing.Optional[str]:
        """return merchant order id."""
        return self.merchantOrderId

    @merchant_order_id.setter
    def merchant_order_id(self, value: typing.Optional[str]) -> None:
        """set merchant order id"""
        self.merchantOrderId = value

    @property
    def success_url(self) -> typing.Optional[str]:
        """return checkout success url ."""
        return self.successUrl

    @success_url.setter
    def success_url(self, value: typing.Optional[str]) -> None:
        """set checkout success url"""
        self.successUrl = value

    @property
    def cancel_url(self):
        """return chechout cancel url"""
        return self.cancelUrl

    @cancel_url.setter
    def cancel_url(self, value: typing.Optional[str]) -> None:
        """set checkout cancel url"""
        self.cancelUrl = value

    @property
    def ipn_url(self) -> typing.Optional[str]:
        """return ipn url."""
        return self.ipnUrl

    @ipn_url.setter
    def ipn_url(self, value: typing.Optional[str]) -> None:
        """set ipn url"""
        self.ipnUrl = value

    @property
    def failure_url(self) -> typing.Optional[str]:
        """return failure url"""
        return self.failureUrl

    @failure_url.setter
    def failure_url(self, value: typing.Optional[str]) -> None:
        """set failure url"""
        self.failureUrl = value

    @property
    def expires_after(self) -> int:
        """return expires after"""
        return self.expiresAfter

    @expires_after.setter
    def expires_after(self, value: int) -> None:
        """set expires after"""
        self.expiresAfter = value

    @property
    def expires_in_days(self) -> int:
        """return expires in days"""
        return self.expiresInDays

    @expires_in_days.setter
    def expires_in_days(self, value: int) -> None:
        """set expires in days"""
        self.expiresInDays = value

    @property
    def total_items_handling_fee(self) -> typing.Optional[float]:
        """return total items handling fee"""
        return self.totalItemsHandlingFee

    @total_items_handling_fee.setter
    def total_items_handling_fee(self, value: typing.Optional[float]) -> None:
        """set total items handling fee"""
        self.totalItemsHandlingFee = value

    @property
    def total_items_delivery_fee(self) -> typing.Optional[float]:
        """return total items delivery fee"""
        return self.totalItemsDeliveryFee

    @total_items_delivery_fee.setter
    def total_items_delivery_fee(self, value: typing.Optional[float]) -> None:
        """set total items delivery fee"""
        self.totalItemsDeliveryFee = value

    @property
    def total_items_discount(self) -> typing.Optional[float]:
        """return total items discount"""
        return self.totalItemsDiscount

    @total_items_discount.setter
    def total_items_discount(self, value: typing.Optional[float]) -> None:
        """set total items discount"""
        self.totalItemsDiscount = value

    @property
    def total_items_tax1(self) -> typing.Optional[float]:
        """return total items tax1"""
        return self.totalItemsTax1

    @total_items_tax1.setter
    def total_items_tax1(self, value: typing.Optional[float]) -> None:
        """set total items tax1"""
        self.totalItemsTax1 = value

    @property
    def total_items_tax2(self) -> typing.Optional[float]:
        """return total items tax2"""
        return self.totalItemsTax2

    @total_items_tax2.setter
    def total_items_tax2(self, value: typing.Optional[float]) -> None:
        """set total items tax2"""
        self.totalItemsTax2 = value

    @property
    def is_sandbox(self) -> bool:
        """return if sandbox is enabled."""
        return self.use_sandbox

    def __setattr__(self, attr, value) -> None:
        """set attribute value."""
        if attr == "_process" and getattr(self, attr, None) is not None:
            raise AttributeError("process type attribute is immutable.")
        super().__setattr__(attr, value)

    def to_dict(self) -> dict:
        data = {}
        attrs = [
            "process",
            "merchantOrderId",
            "merchantId",
            "successUrl",
            "cancelUrl",
            "ipnUrl",
            "failureUrl",
            "expiresAfter",
            "expiresInDays",
            "totalItemsHandlingFee",
            "totalItemsDeliveryFee",
            "totalItemsDiscount",
            "totalItemsTax1",
            "totalItemsTax2",
        ]
        for attr in attrs:
            if getattr(self, attr, None) is not None:
                data[attr] = getattr(self, attr)

        data.update({"items": [item.to_dict() for item in self.items]})

        return data

    def to_json(self) -> str:
        """return json string of checkout object"""
        return json.dumps(self.to_dict())

    def __repr__(self):
        return "<{}Checkout: {} - {}>".format(
            self.process, self.merchant_order_id, self.merchant_id
        )

    def __str__(self):
        return self.__repr__()

    def get_url(self):
        """return checkout url"""

        status_code, response = ApiRequest.checkout(
            self.to_dict(), self.is_sandbox
        )
        if status_code == codes.ok:
            return response["result"]
        else:
            raise CheckoutError(pformat(response))

    def check_pdt_status(self, transaction_id: str):
        """Check pdt status."""
        pdt = PDT(
            self._client,
            self.merchant_order_id,
            transaction_id,
            use_sandbox=self.is_sandbox,
        )
        return pdt.check_status()


class ExpressCheckout(Checkout):
    """A Checkout class that process express"""

    def __init__(self, *args, **kwargs):
        super().__init__(EXPRESS, *args, **kwargs)


class CartCheckout(Checkout):
    """A Checkout class that process cart"""

    def __init__(self, *args, **kwargs):
        super().__init__(CART, *args, **kwargs)

    def add_item(self, item):
        """Add item into a cart."""

        if not isinstance(item, Item):
            raise TypeError(
                "Checkout item type must be yenepay.model.checkout.Item, "
                "got {}".format(type(item).__name__)
            )

        self.items.append(item)

    def add_items(self, *items):
        """Add multiple items into a cart."""

        for item in items:
            self.add_item(item)

"""
YenePay models
"""
import json
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


class Cart:
    """
    Represent a collection of multiple items to be purchased. Add addtional
    functionalityies for items.
    """

    def __init__(self, *items: typing.List[Item]) -> None:
        """
        :param items: Collection of :class:`yenepay.models.checkout.Item` objects
        :type items: List of :class:`yenepay.models.checkout.Item`

        :rtype: :obj:`None`
        """

        self._items = list(items)
        self._total_price = 0
        self._total_quantity = 0
        self._validate()

    def _validate(self) -> None:
        """
        Validate cart configurations, and initialize cart properties.
        """

        for idx, item in enumerate(self._items):
            self.__validate_item(item, idx)
            self._total_price += item.unitPrice
            self._total_quantity += item.quantity

    def __validate_item(
        self, item: Item, idx: typing.Optional[int] = 0
    ) -> None:
        """Validate a single item is valid or not."""

        if not isinstance(item, Item):
            raise TypeError(
                "Items parameter must be type of yenepay.Item,"
                "got {} at index {}".format(type(item).__name__, idx)
            )

    def create_item(
        self,
        name: str,
        unit_price: float,
        quantity: int,
        item_id: typing.Optional[str] = None,
    ) -> Item:
        """
        Create a new Item instance and add into a cart.

        :param name: A unique identifier of the item (SKU, UUID,…)
                that is used to identify the item on the merchant’s
                platform.
        :type name: :func:`str`

        :param unit_price: Amount in ETB currency. Required for Express type
                checkout.
        :type unit_price: :func:`float`

        :param quantity: Quantity of the item. Required for Express type
                checkout.
        :type quantity: :func:`int`

        :param item_id: Optional item id. Required for Express type
                checkout.
        :type item_id: Optional :func:`str`

        :return: Created item
        :rtype: :class:`yenepay.models.checkout.Item`
        """
        itemId = item_id or str(uuid.uuid4())
        item = Item(name, unit_price, quantity, itemId)
        self._items.append(item)

        return item

    def __iter__(self) -> typing.Iterator:
        """return iterator of a given cart."""
        return iter(self._items)

    def __contains__(self, item: Item) -> bool:
        """Check a given item is in the cart."""
        return item in self._items

    def add_item(self, item: Item) -> None:
        """
        Add a single item into a cart.

        :param item: Item to be added into a cart.
        :type item: :class:`yenepay.models.checkout.Item`
        :rtype: :obj:`None`
        """
        self.__validate_item(item)
        self._items.append(item)
        self._total_price += item.unitPrice
        self._total_quantity += item.quantity

    def __iadd__(self, item: Item) -> None:
        """add item into a cart."""
        self.__validate_item(item)
        self._items.append(item)

    def __imul__(self, value: int) -> None:
        """multiply number of items."""
        self._items *= value
        self._total_price *= value
        self._total_quantity *= value

    def __len__(self) -> None:
        """return number of items."""
        return len(self._items)

    def __getitem__(self, postion: int) -> Item:
        """return item at a given postion."""
        return self._items[postion]

    def __repr__(self) -> typing.List:
        """return cart representation."""
        return str(self._items)

    @property
    def total_price(self) -> float:
        """
        :return: cart total price
        :rtype: :func:`float`
        """
        return self._total_price

    @property
    def total_quantity(self) -> int:
        """
        :return: cart total quantity.
        :rtype: :func:`int`
        """
        return self._total_quantity

class Checkout(metaclass=ABCMeta):
    """
    Creates a new payment order on YenePay for the authenticated user and
    redirects to checkout application to complete the payment.
    """

    @abstractmethod
    def __init__(
        self,
        client: str,
        process: str,
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
    ) -> None:
        """YenePay checkout options

        :param client: yenepay.Client instance.
        :type client: :obj:`yenepay.models.client.Client`
        :param process:  Checkout type for this payment. Should have a value
                of either Express or Cart. Use Express checkout type for
                single item payment and Cart if this payment includes more
                than one item.
        :type process: :obj:`str`
        :param items: Items to be purchased.
        :type items: List :obj:`yenepay.models.checkout.Item`
        :param merchant_order_id: A unique identifier for this payment order
                on the merchant’s platform. Will be used to track payment
                status for this order.
        :type merchant_order_id: Optional :obj:`str`
        :param success_url: A fully qualified URL endpoint on the merchant’s
                platform that will be used to redirect the paying customer
                after the payment has successfully been completed.
        :type success_url: Optional :obj:`str`
        :param cancel_url: A fully qualified URL endpoint on the merchant’s
                platform that will be used to redirect the paying
                customer if this payment is cancelled by the customer.
        :type cancel_url: Optional :obj:`str`
        :param ipn_url: A fully qualified URL endpoint on the merchant’s
                platform that will be used to send Instant Payment
                Notification to the merchant’s platform when a payment
                is successfully completed.
        :type ipn_url: Optional :obj:`str`
        :param failure_url: A fully qualified URL endpoint on the merchant’s
                platform that will be used to redirect the paying customer
                if this payment fails.
        :type failure_url: Optional :obj:`str`
        :param expires_after: Expiration period for this payment in minutes.
                This payment order will expire after the specified number
                of minutes, if specified.
        :type expires_after: Optional :obj:`int`
        :param expires_in_days: Expiration period for this payment in days.
                This payment order will expire after the specified number
                of days. The default value is 1 day.
        :type expires_in_days: Optional :obj:`int`
        :param total_items_handling_fee: Handling fee in ETB currency for this
                payment order, if applicable. Set this value for Cart type
                checkout. When calculating total payment amount, this will
                be added to the cart items total amount.
        :type total_items_handling_fee: Optional :obj:`float`
        :param total_items_delivery_fee: Delivery or shipping fee in ETB
                currency for this payment order, if applicable. Set this
                value for Cart type checkout. When calculating total
                payment amount, this will be added to the cart items total
                amount.
        :type total_items_devlivery_fee: Optional :obj:`float`
        :param total_items_discount: Discount amount in ETB currency for this
                payment order, if applicable. Set this value for Cart type
                checkout. When calculating total payment amount, this will
                be deducted from the cart items total amount.
        :type total_items_discount: Optional :obj:`float`
        :param total_items_tax1: Tax amount in ETB currency for this payment
                order, if applicable. Set this value for Cart type
                checkout. When calculating total payment amount, this will
                be added to the cart items total amount.
        :type total_items_tax1: Optional :obj:`float`
        :param total_items_tax2: Tax amount in ETB currency for this payment
                order, if applicable. Set this value for Cart type
                checkout. When calculating total payment amount, this will
                be added to the cart items total amount.
        :type total_items_tax2: Optional :obj:`float`
        """

        self._client = client
        self._process = process
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
        self._validate()

    def _validate(self) -> None:
        """
        validate configuration.
        """

        from yenepay.models.client import Client

        if not isinstance(self._client, Client):
            raise TypeError(
                "client must be instance of yenepay.Client, got {}".format(
                    type(self._client).__name__
                )
            )

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
                "Items must be tuple, set or list, got {}".format(
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
        """set tis_saotal items tax2"""
        self.totalItemsTax2 = value

    @property
    def is_sandbox(self) -> bool:
        """return if sandbox is enabled."""
        return self._client.use_sandbox

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

    def __init__(self, client, *args, **kwargs):
        super().__init__(client, EXPRESS, *args, **kwargs)


class CartCheckout(Checkout):
    """A Checkout class that process cart"""

    def __init__(self, client, *args, **kwargs):
        super().__init__(client, CART, *args, **kwargs)

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

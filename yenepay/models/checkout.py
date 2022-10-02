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
from yenepay.helpers import Validator
from yenepay.models.pdt import PDT


class Item(Validator):
    """
    Represent a single item to be purchased. Item will be used when Express or
    Cart checkout is created.

    .. note:: Item ID is not required, but if not given the class will
              generate new UUID for an item.

    * Sample usage

    >>> from yenepay import Item
    >>>
    >>> # Creating a single item
    >>> item = Item(
            name="PC-1",
            unit_price=42_000.00,
            quantity=1,
        )

    >>> # Or using positional arguments
    >>> item = Item("PC-1", 42_000.00, 1)

    >>> # Creating multiple items
    >>> items = [
            Item("PC-2", 40_000.99, 1),
            Item("PC-3", 40_000.99, 1),
            Item("PC-4", 40_000.99, 1),
            Item("PC-5", 40_000.99, 1),
    ]

    >>> # Or using Cart
    >>> from yenepay import Cart, Item
    >>> cart = Cart(
            Item("PC-6", 50_700.99, 1),
            Item("PC-7", 43_001.99, 1),
        )
    """

    def __init__(
        self,
        name: str,
        unit_price: float,
        quantity: int,
        item_id: typing.Optional[str] = None,
    ) -> None:
        """
        :param name: A unique identifier of the item (SKU, UUID,…)
                that is used to identify the item on the merchant’s
                platform.
        :type name: :func:`str`

        :param unit_price: Amount in ETB currency.
        :type unit_price: :func:`float`

        :param quantity: Quantity of the item.
        :type quantity: :func:`int`

        :param item_id: Optional item id.
        :type item_id: Optional :func:`str`

        :rtype: :obj:`None`
        """

        self.itemId: str = item_id or str(uuid.uuid4())
        self.itemName: str = name
        self.unitPrice: float = unit_price
        self.quantity: int = quantity

    @property
    def id(self) -> typing.Union[str, uuid.UUID]:
        """
        :return: item id
        :rtype: :func:`str` or :class:`uuid.UUID`
        """

        return self.itemId

    @id.setter
    def id(self, value: str):
        """set item id"""
        self.itemId = value

    @property
    def name(self) -> str:
        """
        :return: item name
        :rtype: :func:`str`
        """
        return self.itemName

    @name.setter
    def name(self, value: str):
        """set item name"""
        self.itemName = value

    @property
    def unit_price(self) -> float:
        """
        :return: item unit price
        :rtype: :func:`float`
        """
        return self.unitPrice

    @unit_price.setter
    def unit_price(self, value: float):
        """set item unit price"""
        self.unitPrice = value

    def to_dict(self) -> dict:
        """
        Convert item properties into dictionary object.

        :return: dictionary of item properties.
        :rtype: :func:`dict`
        """
        return {
            attr: getattr(self, attr, None)
            for attr in ["itemId", "itemName", "unitPrice", "quantity"]
            if getattr(self, attr, None) is not None
        }

    def to_json(self) -> bytes:
        """
        Convert item properties into json format. usefull while creating
        requests.

        :return: Json representation of item properties.
        :rtype: :func:`bytes`
        """
        return json.dumps(self.to_dict())

    def __repr__(self) -> str:
        """Item representation."""
        return "<Item '{}'>".format(self.name)

    def __str__(self) -> str:
        """return item string represenation."""
        return self.__repr__()

    def _validate_quantity(self, value: int) -> None:
        """validator item quantity"""
        if value < 1:
            raise ValueError("Item quantity cannot be less than 1")

    def _validate_unitPrice(self, value: float):
        """validate item unit price."""
        if value < 0:
            raise ValueError("Item unit price cannot be negative.")


class Cart(Validator):
    """
    Represent a collection of multiple items to be purchased. Add addtional
    functionalityies for items.
    """

    def __init__(self, *items: typing.List[Item]) -> None:
        """
        :param items: Collection of :class:`yenepay.models.checkout.Item`
                      objects
        :type items: List of :class:`yenepay.models.checkout.Item`

        :raise: TypeError: if one of the items is not an instance of
            :class:`yenepay.models.checkout.Item`
        :rtype: :obj:`None`
        """

        self._total_price: float = 0
        self._total_quantity: int = 0
        self._items: typing.List = list(items)

    def _validate__items(self, value):
        """Validate items attribute."""
        for idx, item in enumerate(value):
            self._validate_item(item, idx)
            self._total_price += item.unitPrice
            self._total_quantity += item.quantity

    def _validate_item(
        self, item: Item, idx: typing.Optional[int] = 0
    ) -> None:
        """Validate a single item is valid or not."""
        if not isinstance(item, Item):
            raise TypeError(
                "Items parameter must be type of yenepay.models.checkout.Item"
                ", got {} at index {}".format(type(item).__name__, idx)
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
        itemId: str = item_id or str(uuid.uuid4())
        item: Item = Item(name, unit_price, quantity, itemId)
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
        self._validate_item(item)
        self._items.append(item)
        self._total_price += item.unitPrice
        self._total_quantity += item.quantity

    def remove_item(self, value: typing.Union[int, str]):
        """
        Remove item from the cart. use item id if string is sent or use
        value as index postion which items are added.

        :param value: item id or position, which is need to be removed.
        :type value: (:func:`int` or :func:`str`)

        :raise Value Error: if a given value of item position or item id is
            invalid.

        :return: item removed from the list
        :rtype: :class:`yenepay.models.checkout.Item`
        """
        item = None
        if isinstance(value, int):
            item = self._items.pop(value)
        elif isinstance(value, str):
            for idx, item in enumerate(self._items):
                if item.id == value:
                    item = self._items.pop(idx)
                    break
        if item is None:
            raise ValueError("Item ID or position is invalid.")

        self._total_price -= item.unit_price
        self._total_quantity -= item.quantity
        return item

    def clear_items(self) -> None:
        """
        Remove all items inside the cart.

        :rtype: :obj:`None`
        """
        self._items.clear()

    def __iadd__(self, item: Item) -> None:
        """add item into a cart."""
        self._validate_item(item)
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


class Checkout(Validator, metaclass=ABCMeta):
    """
    An abstract class to creates a new payment order on YenePay  for a given
    items and generate redirect link to checkout application to complete the
    payment.
    """

    @abstractmethod
    def __init__(
        self,
        client: str,
        process: str,
        items: typing.Union[typing.List[Item], Cart] = [],
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
        """
        :param client: yenepay.Client instance.
        :type client: :class:`yenepay.models.client.Client`

        :param process:  Checkout type for this payment. Should have a value
                of either Express or Cart. Use Express checkout type for
                single item payment and Cart if this payment includes more
                than one item.
        :type process: :func:`str`

        :param items: Items to be purchased.
        :type items: List :class:`yenepay.models.checkout.Item`

        :param merchant_order_id: A unique identifier for this payment order
                on the merchant’s platform. Will be used to track payment
                status for this order.
        :type merchant_order_id: Optional :func:`str`

        :param success_url: A fully qualified URL endpoint on the merchant’s
                platform that will be used to redirect the paying customer
                after the payment has successfully been completed.
        :type success_url: Optional :func:`str`

        :param cancel_url: A fully qualified URL endpoint on the merchant’s
                platform that will be used to redirect the paying
                customer if this payment is cancelled by the customer.
        :type cancel_url: Optional :func:`str`

        :param ipn_url: A fully qualified URL endpoint on the merchant’s
                platform that will be used to send Instant Payment
                Notification to the merchant’s platform when a payment
                is successfully completed.
        :type ipn_url: Optional :func:`str`

        :param failure_url: A fully qualified URL endpoint on the merchant’s
                platform that will be used to redirect the paying customer
                if this payment fails.
        :type failure_url: Optional :func:`str`

        :param expires_after: Expiration period for this payment in minutes.
                This payment order will expire after the specified number
                of minutes, if specified.
        :type expires_after: Optional :func:`int`

        :param expires_in_days: Expiration period for this payment in days.
                This payment order will expire after the specified number
                of days. The default value is 1 day.
        :type expires_in_days: Optional :func:`int`

        :param total_items_handling_fee: Handling fee in ETB currency for this
                payment order, if applicable. Set this value for Cart type
                checkout. When calculating total payment amount, this will
                be added to the cart items total amount.
        :type total_items_handling_fee: Optional :func:`float`

        :param total_items_delivery_fee: Delivery or shipping fee in ETB
                currency for this payment order, if applicable. Set this
                value for Cart type checkout. When calculating total
                payment amount, this will be added to the cart items total
                amount.
        :type total_items_devlivery_fee: Optional :func:`float`

        :param total_items_discount: Discount amount in ETB currency for this
                payment order, if applicable. Set this value for Cart type
                checkout. When calculating total payment amount, this will
                be deducted from the cart items total amount.
        :type total_items_discount: Optional :func:`float`

        :param total_items_tax1: Tax amount in ETB currency for this payment
                order, if applicable. Set this value for Cart type
                checkout. When calculating total payment amount, this will
                be added to the cart items total amount.
        :type total_items_tax1: Optional :func:`float`

        :param total_items_tax2: Tax amount in ETB currency for this payment
                order, if applicable. Set this value for Cart type
                checkout. When calculating total payment amount, this will
                be added to the cart items total amount.
        :type total_items_tax2: Optional :func:`float`

        :raise TypeError:
            - if client attribute is not instance of
                :class:`yenepay.models.client.Client`.
            - if Items are not instance of :func:`list`, :func:`set`,
                :func:`tuple` or :class:`yenepay.models.checkout.Cart`.

        :raise ValueError:
            - if process is :obj:`None` or not :obj:`Express` or :obj:`Cart`.
            - if multiple item is used for
                :obj:`Express` process.

        :rtype: :obj:`None`
        """

        self._client = client
        self._process: str = process
        self.items: typing.List[Item] = items
        self.merchantOrderId: str = merchant_order_id
        self.successUrl: str = success_url
        self.cancelUrl: str = cancel_url
        self.ipnUrl: str = ipn_url
        self.failureUrl: str = failure_url
        self.expiresAfter: int = expires_after
        self.expiresInDays: int = expires_in_days
        self.totalItemsHandlingFee: float = total_items_handling_fee
        self.totalItemsDeliveryFee: float = total_items_delivery_fee
        self.totalItemsDiscount: float = total_items_discount
        self.totalItemsTax1: float = total_items_tax1
        self.totalItemsTax2: float = total_items_tax2

        if not isinstance(self.items, Cart):
            cart = Cart(*(item for item in self.items))
            self.items = cart

    def _validate_client(self, value):
        """validate client attribute."""
        from yenepay.models.client import Client

        if not isinstance(value, Client):
            raise TypeError(
                "client attribute must be instance of yenepay.Client, got "
                "{}".format(type(self._client).__name__)
            )

    def _validate__process(self, value):
        """validate _process attribute."""
        if value is None:
            raise ValueError("Checkout process cannot be None.")

        if value not in (EXPRESS, CART):
            raise ValueError(
                "Process must be {} or {}, got {}".format(EXPRESS, CART, value)
            )

        if getattr(self, "_process", None) is not None:
            raise AttributeError("process type attribute is immutable.")

    def _validate_items(self, value):
        """validate items attribute."""
        if not isinstance(value, (tuple, set, list, Cart)):
            raise TypeError(
                "Items must be tuple, set, list or yenepay.Cart,"
                " got {}".format(type(value).__name__)
            )

        if self.process == EXPRESS and len(value) > 1:
            raise ValueError(
                "'{}' process is for a single item. if you want to "
                "purchase multiple item use '{}' for process"
                " parameter.".format(EXPRESS, CART)
            )

    @property
    def process(self) -> str:
        """
        :return: checkout process type.
        :rtype: :func:`str`
        """
        return getattr(self, "_process", None)

    @property
    def merchant_id(self) -> str:
        """
        :return: checkout merchant id.
        :rtype: :func:`str`
        """
        return self._client.merchantId

    @property
    def merchantId(self) -> str:
        """
        :return: checkout merchant id.
        :rtype: :func:`str`
        """
        return self._client.merchantId

    @property
    def token(self) -> str:
        """
        :return: client pdt token.
        :rtype: :func:`str`
        """
        return self._client.pdtToken

    @property
    def merchant_order_id(self) -> typing.Optional[str]:
        """
        :return: checkout merchant order id.
        :rtype: :func:`str`
        """
        return self.merchantOrderId

    @merchant_order_id.setter
    def merchant_order_id(self, value: typing.Optional[str]) -> None:
        """set merchant order id"""
        self.merchantOrderId = value

    @property
    def success_url(self) -> typing.Optional[str]:
        """
        :return: checkout success url.
        :rtype: :func:`str`
        """
        return self.successUrl

    @success_url.setter
    def success_url(self, value: typing.Optional[str]) -> None:
        """set checkout success url"""
        self.successUrl = value

    @property
    def cancel_url(self):
        """
        :return: chechout cancel url.
        :rtype: :func:`str`
        """
        return self.cancelUrl

    @cancel_url.setter
    def cancel_url(self, value: typing.Optional[str]) -> None:
        """set checkout cancel url"""
        self.cancelUrl = value

    @property
    def ipn_url(self) -> typing.Optional[str]:
        """
        :return: chckout ipn url.
        :rtype: :func:`str`
        """
        return self.ipnUrl

    @ipn_url.setter
    def ipn_url(self, value: typing.Optional[str]) -> None:
        """set ipn url"""
        self.ipnUrl = value

    @property
    def failure_url(self) -> typing.Optional[str]:
        """
        :return: checkout failure url.
        :rtype: :func:`str`
        """
        return self.failureUrl

    @failure_url.setter
    def failure_url(self, value: typing.Optional[str]) -> None:
        """set failure url"""
        self.failureUrl = value

    @property
    def expires_after(self) -> int:
        """
        :return: checkout expires after.
        :rtype: :func:`int`
        """
        return self.expiresAfter

    @expires_after.setter
    def expires_after(self, value: int) -> None:
        """set expires after"""
        self.expiresAfter = value

    @property
    def expires_in_days(self) -> int:
        """
        :return: checkout expires in days.
        :rtype: :func:`int`
        """
        return self.expiresInDays

    @expires_in_days.setter
    def expires_in_days(self, value: int) -> None:
        """set expires in days"""
        self.expiresInDays = value

    @property
    def total_items_handling_fee(self) -> typing.Optional[float]:
        """
        :return: checkout total items handling fee.
        :rtype: :func:`int`
        """
        return self.totalItemsHandlingFee

    @total_items_handling_fee.setter
    def total_items_handling_fee(self, value: typing.Optional[float]) -> None:
        """set total items handling fee"""
        self.totalItemsHandlingFee = value

    @property
    def total_items_delivery_fee(self) -> typing.Optional[float]:
        """
        :return: checkout total items delivery fee.
        :rtype: :func:`float`
        """
        return self.totalItemsDeliveryFee

    @total_items_delivery_fee.setter
    def total_items_delivery_fee(self, value: typing.Optional[float]) -> None:
        """set total items delivery fee"""
        self.totalItemsDeliveryFee = value

    @property
    def total_items_discount(self) -> typing.Optional[float]:
        """
        :return: checkout total items discount
        :rtype: :func:`float`
        """
        return self.totalItemsDiscount

    @total_items_discount.setter
    def total_items_discount(self, value: typing.Optional[float]) -> None:
        """set total items discount"""
        self.totalItemsDiscount = value

    @property
    def total_items_tax1(self) -> typing.Optional[float]:
        """
        :return: checkout total items tax1.
        :rtype: :func:`float`
        """
        return self.totalItemsTax1

    @total_items_tax1.setter
    def total_items_tax1(self, value: typing.Optional[float]) -> None:
        """set total items tax1"""
        self.totalItemsTax1 = value

    @property
    def total_items_tax2(self) -> typing.Optional[float]:
        """
        :return: checkout total items tax2.
        :rtype: :func:`float`
        """
        return self.totalItemsTax2

    @total_items_tax2.setter
    def total_items_tax2(self, value: typing.Optional[float]) -> None:
        """set tis_saotal items tax2"""
        self.totalItemsTax2 = value

    @property
    def is_sandbox(self) -> bool:
        """
        :return: check if sandbox is enabled or not.
        :rtype: :func:`bool`
        """
        return self._client.use_sandbox

    @is_sandbox.setter
    def is_sandbox(self, value: bool) -> None:
        """set client sandbox status"""
        self._client.use_sandbox = value

    @property
    def total_price(self) -> float:
        """
        :return: checkout total price.
        :rtype: :func:`float`
        """
        return self.items.total_price

    @property
    def total_quantity(self) -> int:
        """
        :return: checkout total quantity.
        :rtype: :func:`int`
        """
        return self.items.total_quantity

    def to_dict(self) -> dict:
        """
        Convert checkout properties into dictionary object.

        :return: dictionary of checkout properties
        :rtype: :func:`dict`
        """
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

    def to_json(self) -> bytes:
        """
        Convert checkout properties into json format. usefull while creating
        requests.

        :return: json representaion of checkout properties
        :rtype: :func:`bytes`
        """
        return json.dumps(self.to_dict())

    def __repr__(self):
        """representation of checkout object."""
        return "<{}Checkout: {} - {}>".format(
            self.process, self.merchant_order_id, self.merchant_id
        )

    def __str__(self):
        """string representation of checkout object."""
        return self.__repr__()

    def get_url(self) -> str:
        """
        :return: checkout url for payment order
        :rtype: :func:`str`

        :raise ValueError: if items is empty.
        :raise yenepay.exceptions.CheckoutError: if paramenters
                are incorrect.
        """
        if not self.items:
            raise ValueError("Items cannot be empty")

        status_code, response = ApiRequest.checkout(
            self.to_dict(), self.is_sandbox
        )
        if status_code == codes.ok:
            return response["result"]
        else:
            raise CheckoutError(pformat(response))

    def check_pdt_status(self, transaction_id: str):
        """
        Check pdt status of checkout.

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
            self._client,
            self.merchant_order_id,
            transaction_id,
            use_sandbox=self.is_sandbox,
        )
        return pdt.check_status()


class ExpressCheckout(Checkout):
    """A Checkout class that process express"""

    def __init__(self, client, *args, **kwargs):
        kwargs.pop("process", None)
        items = kwargs.pop("items", None)
        if isinstance(items, Item):
            kwargs.update({"items": [items]})

        super().__init__(client, EXPRESS, *args, **kwargs)

    @property
    def item(self) -> Item:
        """
        :return: an item of express checkout.
        :rtype: :class:`yenepay.models.checkout.Item`
        """
        return self.items[0]


class CartCheckout(Checkout):
    """A Checkout class that process cart"""

    def __init__(self, client, *args, **kwargs):
        kwargs.pop("process", None)
        super().__init__(client, CART, *args, **kwargs)

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
        return self.items.create_item(name, unit_price, quantity, item_id)

    def add_item(self, item):
        """
        Add item into a cart.

        :param item: an item, that need to be added into a cart.
        :type item: :class:`yenepay.models.checkout.Item`

        :rtype: :obj:`None`
        """
        self.items.add_item(item)

    def add_items(self, *items):
        """
        Add multiple items into a cart.

        :param items: list of itmems, that need to be added into a cart.
        :type items: List of :class:`yenepay.models.checkout.Item`

        :rtype: :obj:`None`
        """

        for item in items:
            self.add_item(item)

    def remove_item(self, value: typing.Union[int, str]):
        """
        Remove item from the cart. use item id if string is sent or use
        value as index postion which items are added.

        :param value: item id or position, which is need to be removed.
        :type value: (:func:`int` or :func:`str`)

        :raise ValueError: if number of item in the cart is less than 2.
        :raise Value Error: if a given value of item position or item id is
            invalid.

        :return: item removed from the list
        :rtype: :class:`yenepay.models.checkout.Item`
        """
        return self.items.remove_item(value)

    def clear_items(self) -> None:
        """
        Remove all items inside the cart.

        :rtype: :obj:`None`
        """
        self.items.clear_items()

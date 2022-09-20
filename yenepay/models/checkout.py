"""
YenePay models
"""
import typing


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


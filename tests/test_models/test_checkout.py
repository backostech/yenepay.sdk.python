"""
Test for YenePay checkout
"""
import random
import unittest

from faker import Faker

from yenepay.models.checkout import Checkout as AbstractCheckout, Item

fake = Faker()


def get_random_price():
    """return random price value."""
    return round(random.random() * 10e5, 2)


class Checkout(AbstractCheckout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TestItem(unittest.TestCase):
    """Test item model."""

    def setUp(self):
        self.name = fake.name()
        self.id = fake.uuid4()
        self.unit_price = get_random_price()
        self.quantity = random.randint(1, 10e2)

        self.item = Item(
            name=self.name,
            unit_price=self.unit_price,
            quantity=self.quantity,
            item_id=self.id,
        )

    def test_item_id(self):
        """test item id."""
        self.assertEqual(self.item.id, self.id)
        self.assertEqual(self.item.itemId, self.id)

    def test_item_id_setter(self):
        """test item id setter."""
        item_id = fake.uuid4()
        self.item.id = item_id

        self.assertEqual(self.item.id, item_id)
        self.assertEqual(self.item.itemId, item_id)

    def test_item_name(self):
        """test item name."""
        self.assertEqual(self.item.name, self.name)
        self.assertEqual(self.item.itemName, self.name)

    def test_item_name_setter(self):
        """test item name setter."""
        item_name = fake.name()
        self.item.name = item_name

        self.assertEqual(self.item.name, item_name)
        self.assertEqual(self.item.itemName, item_name)

    def test_item_unit_price(self):
        """test item unit price."""
        self.assertEqual(self.item.unit_price, self.unit_price)
        self.assertEqual(self.item.unitPrice, self.unit_price)

    def test_unit_price_setter(self):
        """test unit price setter."""
        unit_price = get_random_price()
        self.item.unit_price = unit_price

        self.assertEqual(self.item.unit_price, unit_price)
        self.assertEqual(self.item.unitPrice, unit_price)

    def test_item_quantity(self):
        """test item quantity."""
        self.assertEqual(self.item.quantity, self.quantity)

    def test_item_representation(self):
        """test item representation."""
        self.assertEqual(self.item.__repr__(), f"<Item '{self.item.name}'>")

    def test_item_string_representation(self):
        """test item string representation."""
        self.assertEqual(str(self.item), self.item.__repr__())

    def test_to_dict(self):
        """test item to dict."""
        data = {
            "itemId": self.item.itemId,
            "itemName": self.item.itemName,
            "unitPrice": self.item.unitPrice,
            "quantity": self.item.quantity,
        }

        self.assertEqual(self.item.to_dict(), data)


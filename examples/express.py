"""
Create checkout url for express process from client.
"""
from yenepay import Client, Item

client = Client(merchant_id="0000")

item = Item("PC", 42_000.00, 1)

express_checkout = client.get_cart_checkout(items=item)

checkout_url = express_checkout.get_url()

print(checkout_url)

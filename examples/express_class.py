"""
Create checkout url for express process using ExpressCheckout class.
"""
from yenepay import Client, ExpressCheckot, Item

client = Client(merchant_id="0000")

item = Item("PC", 42_000.00, 1)

express_checkout = ExpressCheckot(
    client,
    item,
    use_sandbox=True,
)

checkout_url = express_checkout.get_url()

print(checkout_url)

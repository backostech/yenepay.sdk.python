from yenepay import Client, Item

client = Client(merchant_id="0000", token="abcd")

item = Item("PC", 42_000.00, 1)

express_checkout = client.get_cart_checkout(
    items=[item], merchant_order_id="a1b2c3"
)

checkout_url = express_checkout.get_url()

print(checkout_url)

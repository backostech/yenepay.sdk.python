"""
Create checkout url for cart process using cart instance.
"""
from yenepay import Cart, Client, Item

client = Client(merchant_id="0000")

# Create carts to store items.
cart = Cart(
    Item("PC_1", 50_000.00, 1),
    Item("PC_2", 20_000.00, 3),
    Item("PC_3", 10_000.00, 4),
    Item("PC_4", 150_000.00, 2),
)

cart_checkout = client.get_cart_checkout(items=cart)

checkout_url = cart_checkout.get_url()  # Return link for payment, if success

print(checkout_url)

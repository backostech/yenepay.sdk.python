"""
Check payment order status from checkout instance.
"""
from yenepay import Client, Item

client = Client(merchant_id="0000", token="abcd")

transaction_id = "abcd"

express_checkout = client.get_express_checkout(
    client,
    Item("PC-1", 50_000.00, 1),
    merchant_order_id="0000",
    success_url="localhost:8000",  # Url, transaction id will be sent,
    use_sandbox=True,
)

response = express_checkout.check_pdt_status(transaction_id)

if response.result == "SUCCESS" and response.status == "Paid":
    print("Payment Completed By: {}".format(response.buyer_id))

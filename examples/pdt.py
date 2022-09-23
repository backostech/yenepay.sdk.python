from yenepay import Client

client = Client(merchant_id="0000", token="abcd")

merchant_order_id = "0000"  # Give when you create checkout url

transaction_id = "abcd"  # Send from yenepay when payment is successfull

response = client.check_pdt_status(merchant_order_id, transaction_id)

if response.result == "SUCCESS" and response.status == "Paid":
    print("Payment Completed By: {}".format(response.buyer_id))

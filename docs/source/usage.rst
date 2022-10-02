.. _usage:

######
Usage
######

.. include:: common_terms.rst

Client
======

:obj:`yenepay.models.client.Client` instance represents a single merchant account in YenePay platform.

Creating client
****************

Inorder to create a client instance it is required to have a merchant/seller code. If you don't have one, first need to register on YenePay as a merchant and get your seller code. Read how you would get one from https://community.yenepay.com/docs/getting-started/get-your-seller-merchant-code/

.. code-block:: python

    from yenepay import Client

    client = Client(merchant_id="0000")

If you are going to check PDT status of you payment order, you must provide PDT token for your client instance. You can find your pdt token from your YenePay profile section.

.. code-block:: python

    from yenepay import Client

    client = Client(merchant_id="0000", token="abcd")

When ever you have a sandbox merchant ID and PDT token you must set `use_sanbox=True` while you create instance. Default is set to `False`


.. code-block:: python

    from yenepay import Client

    client = Client("0000", "abcd", use_sandbox=True)

    # You can check whether client is using sanbox or not use `is_sandbox` attribute
    client.is_sandbox # True

.. warning:: If you use sandbox account details (merchant id and/or PDT token) without using `use_sanbox=True` will raise :exc:`yenepay.exceptions.CheckoutError`

Generating checkout url
************************

If you have a client instance you can create checkout url directly using :obj:`yenepay.models.client.Client.get_express_checkout` or :obj:`yenepay.models.client.Client.get_cart_checkout`. You can check function parameters from :obj:`yenepay.models.checkout.Checkout`

Creating express checkout
--------------------------
Using a function :obj:`yenepay.models.client.Client.get_express_checkout` can generate checkout link.

.. code-block:: python

    from yenepay import Client, Item

    client = Client("0000") # send your merchant id as first parameter

    # Create item
    item = Item("PC-1", 34_000.99, 1)

    express_checkout = client.get_express_checkout(item)

    checkout_url = express_checkout.get_url() # returns checkout url

Creating cart checkout
--------------------------
Using a function :obj:`yenepay.models.client.Client.get_cart_checkout` can generate checkout link.

.. code-block:: python

    from yenepay import Cart, Client, Item

    client = Client("0000") # send your merchant id as first parameter

    # Create item
    cart = Cart(
        Item("PC-1", 39_999.99, 1),
        Item("PC-2", 40_000.00, 1),
        Item("PC-3", 55_000.99, 1),
    )

    cart_checkout = client.get_express_checkout(cart)

    checkout_url = cart_checkout.get_url() # returns checkout url

Checking PDT status
********************

If you want to check whether your payment order is paid or not, you can send pdt request to YenePay server using :obj:`yenepay.models.pdt.PDT` class. Before checking you payment order status you need to have `merchant_order_id` and `transaction_id`. You can create `merchant_order_id` when you are creating checkout (express or cart). You can get your transaction id from `success_url` when a payment is completed.

.. code-block:: python

    from yenepay import Client, Item

    client = Client("0000", "abcd")

    mo_id = "m01x"

    # Prepare checkout process
    express_checkout = client.get_express_checkout(
        Item("TV", 13_000.00, 1),
        merchant_order_id=mo_id,
        success_url="localhost:8000",
        # User will redirected to this url after transaction is completed.
        # Required for checking pdt status
    )

    checkout_url = express_checkout.get_url()

    """
    Send `checkout_url` to you customers, and check payment status
    when your `success_url` endpoint is called.
    """

    # return yenepay.PDTResponse instance on success
    pdt_status = client.check_pdt_status(
                mo_id, # merchant order id
                "01cd13eae42", # transaction id
            )

    pdt_status.result # Success

    pdt_status.status # Paid

    pdt_status.buyer_id # 1103cdca12


    # Or you ca checkfrom checkout instance

    pdt_status = express_checkout.check_pdt_status("01cd13eae42") # transaction id

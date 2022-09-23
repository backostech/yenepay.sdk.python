<a href="https://www.yenepay.com"> <img align="left" height="75" src="https://www.yenepay.com/images/logo.png"/></a>
<h1 align="left">ᴘʏᴛʜᴏɴ sᴅᴋ | ᴜɴᴏғғɪᴄɪᴀʟ</h1>

![test-status](https://github.com/backostech/yenepay.sdk.python/actions/workflows/pytest.yml/badge.svg)
![linter-status](https://github.com/backostech/yenepay.sdk.python/actions/workflows/linters.yml/badge.svg)
![publication-status](https://github.com/backostech/yenepay.sdk.python/actions/workflows/python-publish.yml/badge.svg)

This library allows you to quickly and easily add YenePay as a payment method using Python

We encourage you to read through this README to get the most our of what this library has to offer. We want this library to be community driven and we really appreciate any support we can get from the community.

## Getting Started

These instructions will guide you on how to develop and test YenePay's payment method integration with your Python application. YenePay have setup a sandbox environment for you to test and play around the integration process. To learn more about this, please visit yenepay community site: https://community.yenepay.com/

## Pre-requisite

To add YenePay to your application and start collecting payments, you will first need to register on YenePay as a merchant and get your seller code. You can do that from https://www.yenepay.com/merchant

## Installation

### Option 1: Using [PyPI](https://pypi.org/project/yenepay/)
```sh
pip install yenepay
```

### Option 2: Directly from [GitHub](https://github.com:backostech/yenepay.sdk.python)
* Clone package into local folder and change director
```sh
git clone git@github.com:backostech/yenepay.sdk.python.git
cd yenepay.sdk.python/
```
* Install using python `setuptools`
```sh
python setup.py .
```

## Basic Usage

### Creating client
* Inorder to use and feature from this package, first you have to create a client instance.
```python
from yenepay import Client

MERCHANT_ID = "0000"

client = Client(MERCHANT_ID) # Return client instance
```
### Creating express checkout
```python
from yenepay import Client, Item

client = Client(merchant_id="0000", token="abcd")

item = Item("PC", 42_000.00, 1)

express_checkout = client.get_cart_checkout(
    items=[item],
    merchant_order_id="a1b2c3",
    use_sandbox=True,
)

checkout_url = express_checkout.get_url()

print(checkout_url)
```

### Creating cart checkout
```python
from yenepay import Client, Item

MERCHANT_ID = "0000"

client = Client(MERCHANT_ID)

items = [
    Item("PC_1", 50_000.00, 1),
    Item("PC_2", 20_000.00, 3),
    Item("PC_3", 10_000.00, 4),
    Item("PC_4", 150_000.00, 2),
]

cart_checkout = client.get_cart_checkout(items=items)

checkout_url = cart_checkout.get_url()  # Return link for payment, if success
```
### PDT
```python
from yenepay import Client

client = Client(merchant_id="0000", token="abcd")

merchant_order_id = "0000"  # Give when you create checkout url

transaction_id = "abcd"  # Send from yenepay when payment is successfull

response = client.check_pdt_status(merchant_order_id, transaction_id)

if response.result == "SUCCESS" and response.status == "Paid":
    print("Payment Completed By: {}".format(response.buyer_id))
```


* Read more fron the documation [ReadTheDocs](https://yenepay.readthedocs.org).


## Contact

Dont't hesitate to contact us, either in person or through our call centers.

<img align=left width="25" height="25" src="https://img.icons8.com/external-flaticons-lineal-color-flat-icons/64/000000/external-envelop-office-and-office-supplies-flaticons-lineal-color-flat-icons.png"/>

info@backostech.com

<img align=left width="25" height="25" src="https://img.icons8.com/color/48/000000/linkedin.png"/>

<a href="https://www.linkedin.com/company/backos-tech/about/">Backos Technologies</a>

<img align=left width="25" height="25" src="https://img.icons8.com/clouds/100/000000/phone.png"/>

+251910900879

<hr />
<p align="center">
  <img width="150" height="150" src="https://github.com/backostech/.github/raw/main/profile/logo.png">
  <h1 align="center"><a href="https://backostech.com">𝔹𝕒𝕔𝕜𝕠𝕤 𝕋𝕖𝕔𝕙𝕟𝕠𝕝𝕠𝕘𝕚𝕖𝕤</a></h1>

  ```
                                                    ᴀ ᴛᴇᴄʜ ʏᴏᴜ ᴄᴀɴ ᴛʀᴜsᴛ
  ```
</p>
<p align="center">© Copyright <a href="https://backostech.com">Backos Technologies</a>. All Rights Reserved</p>

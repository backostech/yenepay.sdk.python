"""
YenePay constants
"""

EXPRESS = "Express"

CART = "Cart"

CHECKOUT_PRODUCTION_URL = (
    "https://endpoints.yenepay.com/api/urlgenerate/getcheckouturl/"
)

CHECKOUT_SANDBOX_URL = (
    "https://testapi.yenepay.com/api/urlgenerate/getcheckouturl/"
)

PDT_PRODUCTION_URL = "https://endpoints.yenepay.com/api/verify/pdt/"

PDT_SANDBOX_URL = "https://testapi.yenepay.com/api/verify/pdt/"

IPN_PRODUCTION_URL = "https://endpoints.yenepay.com/api/verify/ipn/"

IPN_SANDBOX_URL = "https://testapi.yenepay.com/api/verify/ipn/"

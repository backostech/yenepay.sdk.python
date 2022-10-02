"""
YenePay IPN model
"""
import typing
from pprint import pformat
from urllib.parse import parse_qsl, unquote

from requests import codes

from yenepay.api import ApiRequest
from yenepay.exceptions import IPNError
from yenepay.helpers import to_python_attr


class IPN:
    """
    Verifies the validity and integrity of a received IPN request on your IPN
    endpoint.
    """

    def __init__(
        self,
        total_amount: float,
        buyer_id: str,
        merchant_id: str,
        merchant_order_id: str,
        merchant_code: str,
        transaction_id: str,
        status: str,
        transaction_code: str,
        currency: str,
        signature: str,
        use_sandbox: typing.Optional[bool] = False,
    ):
        """
        :param total_amount: the total amount of this payment in ETB expressed
                as decimal. You will get this value when receiving IPN on your
                IPN url endpoint.
        :type total_amount: :func:`float`

        :param buyer_id: a unique identifier of the paying customer as set in
                YenePay’s platform. You will get this value when receiving IPN
                on your IPN url endpoint.
        :type buyer_id: :func:`str`

        :param merchant_id: your YenePay merchant account code. You will get
                this value when receiving IPN on your IPN url endpoint.
        :type merchant_id: :func:`str`

        :param merchant_order_id: the order id for this payment set on your
                platform.You will get this value when receiving IPN on your
                IPN url endpoint.
        :type merchant_order_id: :func:`str`

        :param merchant_code: your YenePay merchant account code. You will
                get this value when receiving IPN on your IPN url endpoint.
        :type merchant_code: :func:`str`

        :param transaction_id: a unique identifier id of the payment
                transaction that is set on YenePay’s platform. You will get
                this value when receiving IPN on your IPN url endpoint.
        :type transaction_id: :func:`str`

        :param transaction_code: the order code for this transaction that is
                set on YenePay platform. You will get this value when
                receiving IPN on your IPN url endpoint.
        :type transaction_code: :func:`str`

        :param status: the status code of the payment transaction. You will
                get this value when receiving IPN on your IPN url endpoint.
        :type status: :func:`str`

        :param currency: the currency for this payment. Should be se to “ETB”
        :type currency: :func:`str`

        :param signature: the payment signature for this transaction. You will
                get this value when receiving IPN on your IPN url endpoint.
        :type signature: :func:`str`

        :param use_sandbox: Use sandbox environment. Default is False.
        :type use_sandbox: Optional :func:`bool`

        :rtype: :obj:`None`
        """

        self.totalAmount: float = total_amount
        self.buyerId: str = buyer_id
        self.merchantId: str = merchant_id
        self.merchantOrderId: str = merchant_order_id
        self.merchantCode: str = merchant_code
        self.transactionId: str = transaction_id
        self.transactionCode: str = transaction_code
        self.status: str = status
        self.currency: str = currency
        self.signature: str = signature
        self.use_sandbox: bool = use_sandbox

    @property
    def total_amount(self) -> float:
        """
        :return: IPN total amount
        :rtype: :func:`float`
        """
        return self.totalAmount

    @total_amount.setter
    def total_amount(self, value: float) -> None:
        """set ipn total amount"""
        self.totalAmount = value

    @property
    def buyer_id(self) -> str:
        """
        :return: IPN buyer ID
        :rtype: :func:`str`
        """
        return self.buyerId

    @buyer_id.setter
    def buyer_id(self, value: str) -> None:
        """set IPN buyer ID"""
        self.buyerId = value

    @property
    def merchant_id(self) -> str:
        """
        :return: IPN merchant id
        :rtype: :func:`str`
        """
        return self.merchantId

    @merchant_id.setter
    def merchant_id(self, value: str) -> None:
        """set IPN merchant id"""
        self.merchantId = value

    @property
    def merchant_order_id(self) -> str:
        """
        :return: IPN merchant order id
        :rtype: :func:`str`
        """
        return self.merchantOrderId

    @merchant_order_id.setter
    def merchant_order_id(self, value: str) -> None:
        """set IPN merchant order id"""
        self.merchantOrderId = value

    @property
    def merchant_code(self) -> str:
        """
        :return: IPN merchant code
        :rtype: :func:`str`
        """
        return self.merchantCode

    @merchant_code.setter
    def merchant_code(self, value: str) -> None:
        """set IPN merchant code"""
        self.merchantCode = value

    @property
    def transaction_id(self) -> str:
        """
        :return: IPN transaction ID
        :rtype: :func:`str`
        """
        return self.transactionId

    @transaction_id.setter
    def transaction_id(self, value: str) -> None:
        """set IPN transaction ID"""
        self.transactionId = value

    @property
    def transaction_code(self) -> str:
        """
        :return: IPN transaction code
        :rtype: :func:`str`
        """
        return self.transactionCode

    @transaction_code.setter
    def transaction_code(self, value: str) -> None:
        """set IPN transaction code"""
        self.transactionCode = value

    @property
    def is_sandbox(self) -> bool:
        """
        :return: check if sandbox is enabled or not.
        :rtype: :func:`bool`
        """
        return self.use_sandbox

    @is_sandbox.setter
    def is_sandbox(self, value: bool) -> None:
        """set IPN sandbox status"""
        self.use_sandbox = value

    def to_dict(self) -> dict:
        """Convert IPN properties into dictionary object.

        :return: dictionary of IPN property
        :rtype: :func:`dict`
        """

        return {
            attr: getattr(self, attr)
            for attr in [
                "totalAmount",
                "buyerId",
                "merchantOrderId",
                "merchantId",
                "merchantCode",
                "transactionId",
                "status",
                "transactionCode",
                "currency",
                "signature",
            ]
        }

    def is_authentic(self, raise_exception=False) -> bool:
        """verify a given IPN is authentic or not.

        :return: IPN validity
        :rtype: :func:`bool`
        """
        status_code, response = ApiRequest.ipn(self.to_dict(), self.is_sandbox)
        if status_code == codes.ok:
            return True
        elif raise_exception:
            raise IPNError(pformat(response))
        return False

    @classmethod
    def from_str(cls, content: str):
        """
        Buid IPN instance from request body content

        :return: IPN instance
        :rtype: :class:`yenepay.models.ipn.IPN`
        """

        kwargs = {
            to_python_attr(attr): value
            for attr, value in parse_qsl(unquote(content))
        }
        return cls(**kwargs)

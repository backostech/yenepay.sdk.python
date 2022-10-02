Common terms
=============

Understanding the workflow and integration process will be easier if you are familiar with these common terminologies and concepts that are used throughout this document.

* **Merchant/Seller/Receiver** Any user who wants to collect payments or receive money through YenePay

* **Buyer/Sender** An end user or a customer that is making a payment for purchasing a product or service

* **Checkout** Checkout is the process of selecting a payment method and completing a payment.

* **Merchant ID/Seller Code/User Code** This is an ID that is used to uniquely identify a YenePay customer. This is required to successfully integrate with YenePay and track transactions made. A seller code is an all-digit code with a minimum length of 4 digits.

* **Order Code** An Order Code is an ID that is used to uniquely identify a transaction made through YenePay and ties information about the buyer, the merchant, the purchased items and the amount paid. This order code can also be used to get details of the payment made after the payment has been completed.

* **Instant Payment Notification (IPN)** After YenePay processes the payment order initiated from your website or app by your customers, YenePay system sends a notification called Instant Payment Notification (IPN) to your website or app to the IPNUrl you have configured on your YenePay account settings OR the IPNUrl that is sent with the payment request body. It is strongly recommend you have an IPN URL on your website or app ready to accept notifications.

* **Payment Data Transfer (PDT)** Payment Data Transfer is used by merchants to check the current status of an initiated payment order from their sites. This provides an alternative method to check a payment’s current state at any time.

* **Cancel URL** The absolute URL on your site the buyer will be redirected to when a payment process is cancelled.

* **Failure URL** The absolute URL on your site the buyer will be redirected to when an error happens during the payment process.

* **IPN URL**  The absolute URL on your site that will be used to send you IPNs. If this field is left empty when making a request, the default IPN URL you provided on your account’s settings page will be used instead.

* **Success URL** The absolute URL on your site the buyer will be redirected to when the payment process has successfully been completed.

Read from https://community.yenepay.com/docs/getting-started/common-terms/

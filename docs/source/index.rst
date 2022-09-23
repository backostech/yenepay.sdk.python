.. YenePay documentation master file, created by
   sphinx-quickstart on Thu Sep 22 12:54:22 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to YenePay's Python SDK (ᴜɴᴏғғɪᴄɪᴀʟ) documentation!
===========================================================

.. image:: https://www.yenepay.com/images/logo.png
       :target: https://www.yenepay.com
       :height: 25px
       :alt: YenePay

.. image:: https://github.com/backostech/yenepay.sdk.python/actions/workflows/pytest.yml/badge.svg
       :target: https://github.com/backostech/yenepay.sdk.python
       :alt: Test

.. image:: https://github.com/backostech/yenepay.sdk.python/actions/workflows/linters.yml/badge.svg
       :target: https://github.com/backostech/yenepay.sdk.python
       :alt: Linters

.. image:: https://github.com/backostech/yenepay.sdk.python/actions/workflows/python-publish.yml/badge.svg
       :target: https://github.com/backostech/yenepay.sdk.python
       :alt: Publication

This library allows you to quickly and easily add YenePay as a payment method using Python

We encourage you to read through this document to get the most our of what this library has to offer. We want this library to be community driven and we really appreciate any support we can get from the community.

Getting Started
-----------------

These instructions will guide you on how to develop and test YenePay's payment method integration with your Python application. YenePay have setup a sandbox environment for you to test and play around the integration process. To learn more about this, please visit yenepay community site: https://community.yenepay.com/

Pre-requisite
--------------
To add YenePay to your application and start collecting payments, you will first need to register on YenePay as a merchant and get your seller code. You can do that from https://www.yenepay.com/merchant

Quick Start
------------
Install yenepay using `pip`

.. code-block:: bash

    pip install yenepay

Creating basic express checkout

.. literalinclude:: ../../examples/express.py

Creating basic cart checkout

.. literalinclude:: ../../examples/cart.py

Checking PDT Status

.. literalinclude:: ../../examples/pdt.py

Contents
=========
.. toctree::
   :maxdepth: 3

   install/
   api_reference/


* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

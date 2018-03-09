.NET Viewstate Decoder
======================

A small Python 3 library for decoding .NET viewstate. Can be used in various scraping scenarios.

.. image:: https://travis-ci.org/yuvadm/viewstate.svg?branch=master
    :target: https://travis-ci.org/yuvadm/viewstate

Install
-------

.. code-block:: shell

   $ pip install viewstate

Usage
-----

The Viewstate decoder accepts Base64 encoded .NET viewstate data and returns the decoded output in the form of plain Python objects.

There are two main ways to use this package. First, it can be used as an imported library with the following typical use case:

.. code-block:: python

  from viewstate import ViewState
  vs = ViewState(base64EncodedViewState)
  decoded_state = vs.decode()

It is also possible to feed the raw bytes directly:

.. code-block:: python

  vs = ViewState(raw=b'\xff\x01....')

Alternatively, the library can be used via command line by directly executing the module:

.. code-block:: shell

  $ cat data.base64 | python -m viewstate

Which will pretty-print the decoded data structure.

Development
-----------

.. code-block:: shell

  $ pytest

References
----------

- https://github.com/mutantzombie/JavaScript-ViewState-Parser
- http://viewstatedecoder.azurewebsites.net/

License
-------
MIT

.NET Viewstate Decoder
======================

A small Python library for decoding .NET viewstate. Can be used in various scraping scenarios.

Usage
-----

The Viewstate decoder accepts Base64 encoded .NET viewstate data and returns the decoded output in the form of plain Python objects.

There are two main ways to use this package. First, it can be used as an imported library with the following typical use case:

::

  from viewstate import ViewState
  vs = ViewState(base64EncodedViewState)
  decoded_state = vs.decode()

Alternatively, the library can be used via command line by executing the model:

::

  $ cat data.base64 | python -m viewstate

Which will pretty-print the decoded data structure.

Development
-----------

Unit test are run via `pytest`

References
----------

- https://github.com/mutantzombie/JavaScript-ViewState-Parser
- http://viewstatedecoder.azurewebsites.net/

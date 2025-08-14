IB Data SDK Documentation
========================

A Python SDK for retrieving historical market data from Interactive Brokers.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   quickstart
   api/index
   examples/index
   changelog

Features
--------

* 🚀 **Easy to use**: Simple, intuitive API for data retrieval
* 🔧 **Extensible**: Plugin architecture for custom data processors  
* 📊 **Pandas integration**: Built-in DataFrame support
* 🛡️ **Type safe**: Full type hints and Pydantic validation
* 📱 **CLI included**: Command-line interface for quick data retrieval
* 🏗️ **Production ready**: Proper error handling, logging, and testing

Quick Example
-------------

.. code-block:: python

   from ib_data_sdk import IBDataClient, HistoricalDataRequest
   from ib_data_sdk.enums import Duration, BarSize, DataType

   # Create client and request
   client = IBDataClient()
   request = HistoricalDataRequest(
       symbol="AAPL",
       duration=Duration.DAY_1,
       bar_size=BarSize.MIN_5,
       data_type=DataType.TRADES
   )

   # Get data
   df = client.get_historical_data_as_dataframe(request)
   print(df.head())

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

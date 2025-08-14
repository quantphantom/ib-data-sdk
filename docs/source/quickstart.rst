Quick Start Guide
=================

This guide will get you up and running with the IB Data SDK in minutes.

Installation
------------

Install the SDK using pip:

.. code-block:: bash

   pip install ib-data-sdk

For development:

.. code-block:: bash

   pip install ib-data-sdk[dev]

Setup
-----

Environment Variables
~~~~~~~~~~~~~~~~~~~~~

Set up your Interactive Brokers connection parameters:

.. code-block:: bash

   export TWS_HOST=127.0.0.1
   export TWS_PORT=7497  # Paper trading port (7496 for live)
   export TWS_CLIENT_ID=1

Interactive Brokers Setup
~~~~~~~~~~~~~~~~~~~~~~~~~

1. Install and start TWS (Trader Workstation) or IB Gateway
2. Enable API connections in TWS: Configure → API → Settings
3. Add your client ID to the trusted clients list
4. Make sure the socket port matches your TWS_PORT

Basic Usage
-----------

Simple Data Retrieval
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from ib_data_sdk import IBDataClient, HistoricalDataRequest
   from ib_data_sdk.enums import Duration, BarSize, DataType

   # Create client
   client = IBDataClient()

   # Create request
   request = HistoricalDataRequest(
       symbol="AAPL",
       duration=Duration.DAY_1, 
       bar_size=BarSize.MIN_5,
       data_type=DataType.TRADES
   )

   # Get data as DataFrame
   df = client.get_historical_data_as_dataframe(request)
   print(df.head())

   # Clean up
   client.disconnect_from_ib()

Using Context Manager
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from ib_data_sdk import IBDataClient

   with IBDataClient() as client:
       df = client.get_historical_data_as_dataframe(request)
       print(f"Retrieved {len(df)} records")

Command Line Usage
------------------

The SDK includes a CLI for quick data retrieval:

.. code-block:: bash

   # Get 1 day of AAPL data
   ib-data get-data AAPL

   # Customize parameters
   ib-data get-data AAPL --duration DAY_1 --bar-size MIN_1 --data-type BID_ASK

   # Save to file
   ib-data get-data AAPL --output aapl_data.csv

   # List available options
   ib-data list-enums

Next Steps
----------

* Check out the :doc:`examples/index` for more advanced usage
* Read the :doc:`api/index` for detailed API documentation
* Learn about custom processors in :doc:`examples/custom_processors`
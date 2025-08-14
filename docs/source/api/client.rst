Client API
==========

.. automodule:: ib_data_sdk.client
   :members:
   :undoc-members:
   :show-inheritance:

IBDataClient
------------

.. autoclass:: ib_data_sdk.client.IBDataClient
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__

   .. automethod:: connect_to_ib
   .. automethod:: disconnect_from_ib
   .. automethod:: get_historical_data
   .. automethod:: get_historical_data_as_dataframe

Usage Examples
--------------

Basic Connection
~~~~~~~~~~~~~~~~

.. code-block:: python

   from ib_data_sdk import IBDataClient

   # Using environment variables
   client = IBDataClient()

   # Or specify connection parameters
   client = IBDataClient(
       host="127.0.0.1",
       port=7497,
       client_id=1
   )

Error Handling
~~~~~~~~~~~~~~

.. code-block:: python

   from ib_data_sdk.exceptions import ConnectionError, TimeoutError

   try:
       client.connect_to_ib()
   except ConnectionError as e:
       print(f"Failed to connect: {e}")
   except TimeoutError as e:
       print(f"Connection timeout: {e}")
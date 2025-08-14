import pytest
from unittest.mock import patch, Mock
import pandas as pd

from ib_data_sdk import IBDataClient, HistoricalDataRequest
from ib_data_sdk.enums import Duration, BarSize, DataType


@pytest.mark.integration
class TestEndToEnd:
    """End-to-end integration tests."""

    @patch("ib_data_sdk.client.EClient.__init__")
    @patch("ib_data_sdk.client.Thread")
    def test_full_workflow(
        self, mock_thread, mock_eclient_init, mock_env_vars, sample_trades_data
    ):
        """Test complete workflow from request to DataFrame."""
        # Create client
        client = IBDataClient()

        # Mock IB API interactions
        client.connect = Mock()
        client.run = Mock()
        client.isConnected = Mock(return_value=True)
        client.disconnect = Mock()
        client.reqHistoricalData = Mock()

        # Mock events
        client.connected_event = Mock()
        client.connected_event.wait = Mock(return_value=True)
        client.data_ready_event = Mock()
        client.data_ready_event.wait = Mock(return_value=True)

        # Set up data
        client.records = sample_trades_data.copy()

        # Create request
        request = HistoricalDataRequest(
            symbol="AAPL",
            duration=Duration.DAY_1,
            bar_size=BarSize.MIN_5,
            data_type=DataType.TRADES,
        )

        # Execute workflow
        with patch(
            "ib_data_sdk.client.ContractHandler.create_contract_from_request"
        ), patch(
            "ib_data_sdk.client.DataProcessorFactory.create_processor"
        ) as mock_factory:

            mock_processor = Mock()
            mock_factory.return_value = mock_processor

            df = client.get_historical_data_as_dataframe(request)

            # Verify results
            assert isinstance(df, pd.DataFrame)
            assert len(df) == 2
            assert df.index.name == "date"

            # Verify API calls
            client.reqHistoricalData.assert_called_once()
            mock_factory.create_processor.assert_called_once_with(DataType.TRADES)

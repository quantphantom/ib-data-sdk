import pytest
from unittest.mock import Mock, patch, MagicMock
from threading import Event
import pandas as pd

from ib_data_sdk.client import IBDataClient
from ib_data_sdk.exceptions import ConnectionError, DataRequestError, TimeoutError, ValidationError


class TestIBDataClient:
    """Test suite for IBDataClient."""

    def test_init_with_env_vars(self, mock_env_vars):
        """Test client initialization with environment variables."""
        client = IBDataClient()
        assert client.host == "127.0.0.1"
        assert client.port == 7497
        assert client.client_id == 1

    def test_init_with_params(self):
        """Test client initialization with explicit parameters."""
        client = IBDataClient(host="192.168.1.100", port=7496, client_id=2)
        assert client.host == "192.168.1.100"
        assert client.port == 7496
        assert client.client_id == 2

    @patch('ib_data_sdk.client.EClient.__init__')
    @patch('ib_data_sdk.client.Thread')
    def test_connect_success(self, mock_thread, mock_eclient_init, mock_env_vars):
        """Test successful connection to IB."""
        # Setup mocks
        mock_thread_instance = Mock()
        mock_thread.return_value = mock_thread_instance
        
        client = IBDataClient()
        
        # Mock the connection methods
        client.connect = Mock()
        client.run = Mock()
        client.isConnected = Mock(return_value=True)
        client.connected_event = Mock()
        client.connected_event.wait = Mock(return_value=True)

        # Test connection
        result = client.connect_to_ib()
        
        assert result is True
        assert client.is_connected is True
        client.connect.assert_called_once_with("127.0.0.1", 7497, 1)
        mock_thread_instance.start.assert_called_once()

    @patch('ib_data_sdk.client.EClient.__init__')
    def test_connect_timeout(self, mock_eclient_init, mock_env_vars):
        """Test connection timeout."""
        client = IBDataClient(timeout=1)
        client.connect = Mock()
        client.run = Mock()
        client.connected_event = Mock()
        client.connected_event.wait = Mock(return_value=False)  # Timeout
        
        with patch('ib_data_sdk.client.Thread'):
            with pytest.raises(ConnectionError, match="Connection timeout"):
                client.connect_to_ib()

    def test_disconnect(self, mock_ib_client):
        """Test disconnection from IB."""
        mock_ib_client.isConnected = Mock(return_value=True)
        mock_ib_client.disconnect = Mock()
        
        mock_ib_client.disconnect_from_ib()
        
        mock_ib_client.disconnect.assert_called_once()
        assert mock_ib_client.is_connected is False

    def test_get_historical_data_success(self, mock_ib_client, sample_historical_request, sample_trades_data):
        """Test successful historical data retrieval."""
        # Setup mocks
        mock_ib_client.reqHistoricalData = Mock()
        mock_ib_client.data_ready_event = Mock()
        mock_ib_client.data_ready_event.wait = Mock(return_value=True)
        mock_ib_client.records = sample_trades_data.copy()
        
        with patch('ib_data_sdk.client.ContractHandler.create_contract_from_request') as mock_contract, \
             patch('ib_data_sdk.client.DataProcessorFactory.create_processor') as mock_processor:
            
            mock_contract.return_value = Mock()
            mock_processor.return_value = Mock()
            
            response = mock_ib_client.get_historical_data(sample_historical_request)
            
            assert response.record_count == 2
            assert len(response.data) == 2
            assert response.request == sample_historical_request

    def test_get_historical_data_validation_error(self, mock_ib_client):
        """Test validation error in historical data request."""
        invalid_request = Mock()
        invalid_request.dict = Mock(side_effect=ValueError("Invalid request"))
        
        with pytest.raises(ValidationError, match="Invalid request"):
            mock_ib_client.get_historical_data(invalid_request)

    def test_get_historical_data_timeout(self, mock_ib_client, sample_historical_request):
        """Test timeout in historical data request."""
        mock_ib_client.data_ready_event = Mock()
        mock_ib_client.data_ready_event.wait = Mock(return_value=False)  # Timeout
        
        with patch('ib_data_sdk.client.ContractHandler.create_contract_from_request'), \
             patch('ib_data_sdk.client.DataProcessorFactory.create_processor'):
            
            with pytest.raises(TimeoutError, match="Data request timed out"):
                mock_ib_client.get_historical_data(sample_historical_request, timeout=1)

    def test_get_historical_data_as_dataframe(self, mock_ib_client, sample_historical_request, sample_trades_data):
        """Test getting historical data as DataFrame."""
        # Mock get_historical_data method
        mock_response = Mock()
        mock_response.data = sample_trades_data
        mock_ib_client.get_historical_data = Mock(return_value=mock_response)
        
        df = mock_ib_client.get_historical_data_as_dataframe(sample_historical_request)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert df.index.name == 'date'

    def test_error_handling(self, mock_ib_client):
        """Test IB API error handling."""
        # Test different error codes
        mock_ib_client.error(1, 2104, "Market data farm connection is OK")  # Should not raise
        mock_ib_client.error(1, 321, "Market data farm connection is bad")   # Should not raise
        mock_ib_client.error(1, 502, "Historical Market Data Service error") # Should not raise
        mock_ib_client.error(1, 9999, "Unknown error")                      # Should not raise

    def test_next_valid_id_callback(self, mock_ib_client):
        """Test nextValidId callback."""
        mock_ib_client.connected_event = Mock()
        
        mock_ib_client.nextValidId(100)
        
        assert mock_ib_client.next_order_id == 100
        mock_ib_client.connected_event.set.assert_called_once()

    def test_historical_data_callback(self, mock_ib_client, mock_bar_data):
        """Test historicalData callback."""
        mock_processor = Mock()
        mock_processor.process_bar_data = Mock(return_value={"test": "data"})
        mock_ib_client.current_processor = mock_processor
        mock_ib_client.records = []
        
        mock_ib_client.historicalData(1, mock_bar_data)
        
        assert len(mock_ib_client.records) == 1
        assert mock_ib_client.records[0] == {"test": "data"}
        mock_processor.process_bar_data.assert_called_once_with(mock_bar_data)

    def test_historical_data_end_callback(self, mock_ib_client):
        """Test historicalDataEnd callback."""
        mock_ib_client.data_ready_event = Mock()
        
        mock_ib_client.historicalDataEnd(1, "20240115", "20240116")
        
        mock_ib_client.data_ready_event.set.assert_called_once()

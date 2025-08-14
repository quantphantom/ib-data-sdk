import pytest
import os
from unittest.mock import Mock, MagicMock, patch
import pandas as pd
from datetime import datetime
from threading import Event

from ib_data_sdk import IBDataClient, HistoricalDataRequest
from ib_data_sdk.enums import AssetType, BarSize, Duration, DataType
from ib_data_sdk.processors import TradesDataProcessor, BidAskDataProcessor


@pytest.fixture
def mock_env_vars():
    """Mock environment variables for testing."""
    env_vars = {"TWS_HOST": "127.0.0.1", "TWS_PORT": "7497", "TWS_CLIENT_ID": "1"}
    with patch.dict(os.environ, env_vars):
        yield env_vars


@pytest.fixture
def sample_historical_request():
    """Create a sample historical data request."""
    return HistoricalDataRequest(
        symbol="AAPL",
        duration=Duration.DAY_1,
        bar_size=BarSize.MIN_5,
        asset_type=AssetType.STK,
        exchange="SMART",
        data_type=DataType.TRADES,
    )


@pytest.fixture
def sample_options_request():
    """Create a sample options data request."""
    return HistoricalDataRequest(
        symbol="AAPL",
        duration=Duration.DAY_1,
        bar_size=BarSize.MIN_5,
        asset_type=AssetType.OPT,
        exchange="SMART",
        data_type=DataType.TRADES,
        expiry="20240119",
        strike=150.0,
        right="C",
    )


@pytest.fixture
def mock_bar_data():
    """Mock BarData object from IB API."""
    mock_bar = Mock()
    mock_bar.date = "20240115 09:30:00"
    mock_bar.open = 150.25
    mock_bar.high = 151.50
    mock_bar.low = 149.75
    mock_bar.close = 150.80
    mock_bar.volume = 1000
    return mock_bar


@pytest.fixture
def sample_trades_data():
    """Sample processed trades data."""
    return [
        {
            "date": "20240115 09:30:00",
            "open": 150.25,
            "high": 151.50,
            "low": 149.75,
            "close": 150.80,
            "volume": 1000,
        },
        {
            "date": "20240115 09:35:00",
            "open": 150.80,
            "high": 151.20,
            "low": 150.10,
            "close": 150.90,
            "volume": 800,
        },
    ]


@pytest.fixture
def sample_dataframe(sample_trades_data):
    """Sample pandas DataFrame."""
    df = pd.DataFrame(sample_trades_data)
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)
    return df


@pytest.fixture
def mock_ib_client(mock_env_vars):
    """Mock IBDataClient with connection methods patched."""
    with patch("ib_data_sdk.client.EClient.__init__"), patch(
        "ib_data_sdk.client.IBDataClient.connect"
    ), patch("ib_data_sdk.client.IBDataClient.run"), patch(
        "ib_data_sdk.client.IBDataClient.isConnected", return_value=True
    ):

        client = IBDataClient()
        client.connected_event = Mock()
        client.connected_event.wait = Mock(return_value=True)
        client.is_connected = True
        yield client


@pytest.fixture
def mock_contract():
    """Mock IB contract object."""
    mock_contract = Mock()
    mock_contract.symbol = "AAPL"
    mock_contract.secType = "STK"
    mock_contract.exchange = "SMART"
    mock_contract.currency = "USD"
    return mock_contract


class MockThread:
    """Mock thread that doesn't actually start."""

    def __init__(self, target=None, daemon=None):
        self.target = target
        self.daemon = daemon

    def start(self):
        pass


@pytest.fixture
def mock_thread():
    """Mock threading.Thread."""
    with patch("ib_data_sdk.client.Thread", MockThread):
        yield

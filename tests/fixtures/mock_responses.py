from unittest.mock import Mock
from typing import List, Dict, Any


def create_mock_bar_data(date: str, ohlcv: List[float]) -> Mock:
    """Create mock BarData object."""
    mock_bar = Mock()
    mock_bar.date = date
    mock_bar.open, mock_bar.high, mock_bar.low, mock_bar.close, mock_bar.volume = ohlcv
    return mock_bar


def create_sample_bars() -> List[Mock]:
    """Create sample bar data for testing."""
    return [
        create_mock_bar_data(
            "20240115 09:30:00", [150.25, 151.50, 149.75, 150.80, 1000]
        ),
        create_mock_bar_data(
            "20240115 09:35:00", [150.80, 151.20, 150.10, 150.90, 800]
        ),
        create_mock_bar_data(
            "20240115 09:40:00", [150.90, 151.10, 150.30, 150.70, 1200]
        ),
    ]

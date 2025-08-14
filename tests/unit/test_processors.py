import pytest
from unittest.mock import Mock

from ib_data_sdk.processors import (
    TradesDataProcessor,
    BidAskDataProcessor,
    MidpointDataProcessor,
    DataProcessorFactory,
)
from ib_data_sdk.enums import DataType


class TestDataProcessors:
    """Test suite for data processors."""

    def test_trades_processor(self, mock_bar_data):
        """Test TradesDataProcessor."""
        processor = TradesDataProcessor()

        result = processor.process_bar_data(mock_bar_data)

        expected = {
            "date": "20240115 09:30:00",
            "open": 150.25,
            "high": 151.50,
            "low": 149.75,
            "close": 150.80,
            "volume": 1000,
        }
        assert result == expected
        assert processor.get_data_type() == DataType.TRADES

    def test_bidask_processor(self, mock_bar_data):
        """Test BidAskDataProcessor."""
        processor = BidAskDataProcessor()

        result = processor.process_bar_data(mock_bar_data)

        expected = {
            "date": "20240115 09:30:00",
            "bid_price": 150.25,
            "ask_price": 151.50,
            "bid_size": 149,  # int conversion of 149.75
            "ask_size": 150,  # int conversion of 150.80
        }
        assert result == expected
        assert processor.get_data_type() == DataType.BID_ASK

    def test_midpoint_processor(self, mock_bar_data):
        """Test MidpointDataProcessor."""
        processor = MidpointDataProcessor()

        result = processor.process_bar_data(mock_bar_data)

        expected = {
            "date": "20240115 09:30:00",
            "midpoint": (150.25 + 151.50) / 2,
            "volume": 1000,
        }
        assert result == expected
        assert processor.get_data_type() == DataType.MIDPOINT


class TestDataProcessorFactory:
    """Test suite for DataProcessorFactory."""

    def test_create_trades_processor(self):
        """Test creating trades processor."""
        processor = DataProcessorFactory.create_processor(DataType.TRADES)
        assert isinstance(processor, TradesDataProcessor)

    def test_create_bidask_processor(self):
        """Test creating bid/ask processor."""
        processor = DataProcessorFactory.create_processor(DataType.BID_ASK)
        assert isinstance(processor, BidAskDataProcessor)

    def test_create_midpoint_processor(self):
        """Test creating midpoint processor."""
        processor = DataProcessorFactory.create_processor(DataType.MIDPOINT)
        assert isinstance(processor, MidpointDataProcessor)

    def test_unsupported_processor(self):
        """Test error for unsupported processor type."""
        with pytest.raises(ValueError, match="Unsupported data type"):
            DataProcessorFactory.create_processor(DataType.BID)  # Not implemented

    def test_register_custom_processor(self):
        """Test registering custom processor."""

        class CustomProcessor:
            def get_data_type(self):
                return DataType.BID

        DataProcessorFactory.register_processor(DataType.BID, CustomProcessor)

        processor = DataProcessorFactory.create_processor(DataType.BID)
        assert isinstance(processor, CustomProcessor)

import pytest
from pydantic import ValidationError as PydanticValidationError

from ib_data_sdk.models import HistoricalDataRequest, HistoricalDataResponse
from ib_data_sdk.enums import AssetType, BarSize, Duration, DataType


class TestHistoricalDataRequest:
    """Test suite for HistoricalDataRequest model."""

    def test_valid_stock_request(self):
        """Test valid stock request creation."""
        request = HistoricalDataRequest(
            symbol="AAPL",
            duration=Duration.DAY_1,
            bar_size=BarSize.MIN_5,
            data_type=DataType.TRADES,
        )

        assert request.symbol == "AAPL"
        assert request.asset_type == AssetType.STK  # Default
        assert request.exchange == "SMART"  # Default

    def test_valid_options_request(self):
        """Test valid options request creation."""
        request = HistoricalDataRequest(
            symbol="AAPL",
            asset_type=AssetType.OPT,
            expiry="20240119",
            strike=150.0,
            right="C",
        )

        assert request.asset_type == AssetType.OPT
        assert request.expiry == "20240119"
        assert request.strike == 150.0
        assert request.right == "C"

    def test_symbol_validation(self):
        """Test symbol validation."""
        # Empty symbol should raise error
        with pytest.raises(PydanticValidationError, match="Symbol cannot be empty"):
            HistoricalDataRequest(symbol="")

        # Whitespace-only symbol should raise error
        with pytest.raises(PydanticValidationError, match="Symbol cannot be empty"):
            HistoricalDataRequest(symbol="   ")

    def test_symbol_normalization(self):
        """Test symbol is normalized to uppercase."""
        request = HistoricalDataRequest(symbol="  aapl  ")
        assert request.symbol == "AAPL"

    def test_expiry_validation(self):
        """Test expiry date validation."""
        with pytest.raises(
            PydanticValidationError, match="Expiry must be in YYYYMMDD format"
        ):
            HistoricalDataRequest(
                symbol="AAPL",
                asset_type=AssetType.OPT,
                expiry="2024-01-19",  # Wrong format
                strike=150.0,
                right="C",
            )

    def test_option_right_validation(self):
        """Test option right validation."""
        # Valid rights
        for right in ["C", "P", "CALL", "PUT"]:
            request = HistoricalDataRequest(
                symbol="AAPL",
                asset_type=AssetType.OPT,
                expiry="20240119",
                strike=150.0,
                right=right,
            )
            assert request.right in ["C", "P", "CALL", "PUT"]

        # Invalid right
        with pytest.raises(
            PydanticValidationError, match="Right must be C, P, CALL, or PUT"
        ):
            HistoricalDataRequest(
                symbol="AAPL",
                asset_type=AssetType.OPT,
                expiry="20240119",
                strike=150.0,
                right="X",
            )


class TestHistoricalDataResponse:
    """Test suite for HistoricalDataResponse model."""

    def test_response_creation(self, sample_historical_request, sample_trades_data):
        """Test response model creation."""
        response = HistoricalDataResponse(
            request=sample_historical_request,
            data=sample_trades_data,
            record_count=len(sample_trades_data),
        )

        assert response.request == sample_historical_request
        assert response.data == sample_trades_data
        assert response.record_count == 2
        assert response.retrieved_at is not None

from datetime import datetime, timezone
from unittest import TestCase
from unittest.mock import MagicMock, patch

from requests import Response

from tests.test_utils.requests_utils import (
    EXPECTED_PRICE_DATA_CURRENCY,
    EXPECTED_PRICE_DATA_LAST,
    mock_api_call,
)
from vistafetch.model import Fund
from vistafetch.model.asset import PriceData
from vistafetch.model.asset.financial_asset import FinancialAsset


class TestFinancialAsset(TestCase):
    def test_price_data_not_implemented(self):
        test_input = {
            "displayType": "UNKNOWN",
            "entityType": None,
            "isin": "DE00000000",
            "name": "demon",
            "symbol": "TEST",
            "tinyName": "demon",
            "wkn": "TEST00",
        }

        with self.assertRaises(NotImplementedError):
            FinancialAsset.model_validate(test_input).price_data

    @patch("vistafetch.model.asset.financial_asset.api_session")
    def test_price_data_invalid_response(self, session_mock: MagicMock):
        session_mock.get.return_value = Response()
        session_mock.get.return_value.status_code = 400

        test_input = {
            "displayType": "fund",
            "entityType": "FUND",
            "isin": "DE00000000",
            "name": "demon",
            "symbol": "TEST",
            "tinyName": "demon",
            "wkn": "TEST00",
        }

        with self.assertRaises(RuntimeError):
            Fund.model_validate(test_input).price_data

    @patch("vistafetch.model.asset.financial_asset.api_session")
    def test_price_data_unexpected_response(self, session_mock: MagicMock):
        session_mock.get.return_value.json.return_value = {}

        test_input = {
            "displayType": "fund",
            "entityType": "FUND",
            "isin": "DE00000000",
            "name": "demon",
            "symbol": "TEST",
            "tinyName": "demon",
            "wkn": "TEST00",
        }

        with self.assertRaises(ValueError):
            Fund.model_validate(test_input).price_data

    @patch(
        "vistafetch.model.asset.financial_asset.api_session.get",
        side_effect=mock_api_call,
    )
    def test_price_data(self, session_mock: MagicMock):
        test_input = {
            "displayType": "fund",
            "entityType": "FUND",
            "isin": "DE00000000",
            "name": "demon",
            "symbol": "TEST",
            "tinyName": "demon",
            "wkn": "TEST00",
        }

        fund = Fund.model_validate(test_input)
        result = fund.price_data

        self.assertTrue(isinstance(result, PriceData))
        self.assertEqual(EXPECTED_PRICE_DATA_CURRENCY, result.currency_symbol)
        self.assertEqual(EXPECTED_PRICE_DATA_LAST, result.last)
        self.assertEqual(
            datetime(
                year=2023,
                month=8,
                day=25,
                hour=7,
                minute=0,
                second=21,
                microsecond=999000,
                tzinfo=timezone.utc,
            ),
            result.datetime_open,
        )
        self.assertIsNotNone(fund.market.id_notation)

    @patch(
        "vistafetch.model.asset.financial_asset.api_session.get",
        side_effect=mock_api_call,
    )
    def test_price_data_get_latest_price_data(self, session_mock: MagicMock):
        test_input = {
            "displayType": "fund",
            "entityType": "FUND",
            "isin": "DE00000000",
            "name": "demon",
            "symbol": "TEST",
            "tinyName": "demon",
            "wkn": "TEST00",
        }

        result = Fund.model_validate(test_input).get_latest_price_data()
        self.assertEqual(EXPECTED_PRICE_DATA_CURRENCY, result.currency_symbol)
        self.assertEqual(EXPECTED_PRICE_DATA_LAST, result.last)

    @patch(
        "vistafetch.model.asset.financial_asset.api_session.get",
        side_effect=mock_api_call,
    )
    def test_price_data_get_one_day_price_data(self, session_mock: MagicMock):
        test_input = {
            "displayType": "fund",
            "entityType": "FUND",
            "isin": "DE00000000",
            "name": "demon",
            "symbol": "TEST",
            "tinyName": "demon",
            "wkn": "TEST00",
        }

        result = Fund.model_validate(test_input).get_day_price_data(
            day=datetime.today()
        )
        self.assertTrue(isinstance(result, PriceData))
        self.assertEqual(
            datetime(year=2023, month=10, day=13, hour=12), result.datetime_high
        )
        self.assertEqual(EXPECTED_PRICE_DATA_LAST, result.last)

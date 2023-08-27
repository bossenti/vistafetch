from unittest import TestCase
from unittest.mock import MagicMock, call, patch

from vistafetch.model import Fund, SearchResult

test_input = {
    "expires": 1693078155706,
    "searchValue": "some_term",
    "list": [
        {
            "displayType": "fund",
            "entityType": "FUND",
            "isin": "DE00000000",
            "name": "demon",
            "symbol": "TEST",
            "tinyName": "demon",
            "wkn": "TEST00",
        }
    ],
}


class TestGet(TestCase):
    def test_get(self):
        result = SearchResult.model_validate(test_input).get()
        self.assertTrue(isinstance(result, Fund))
        self.assertEqual("TEST00", result.wkn)

    def test_get_empty_assets(self):
        test_input_no_assets = test_input.copy()
        test_input_no_assets["list"] = []

        with self.assertRaises(RuntimeError):
            SearchResult.model_validate(test_input_no_assets).get()

    def test_get_invalid_index(self):
        with self.assertRaises(AttributeError):
            SearchResult.model_validate(test_input).get(5)


class TestVisualize(TestCase):
    @patch("vistafetch.model.search_result.Console")
    @patch("vistafetch.model.search_result.Table")
    def test_visualize(self, table_mock: MagicMock, console_mock: MagicMock):
        result = SearchResult.model_validate(test_input)
        result.visualize()

        self.assertIn(call(title="Financial assets discovered"), table_mock.mock_calls)

        self.assertIn(
            call().add_column("Index", justify="center"), table_mock.mock_calls
        )
        self.assertIn(
            call().add_column("Name", justify="center"), table_mock.mock_calls
        )
        self.assertIn(
            call().add_column("Asset Type", justify="center"), table_mock.mock_calls
        )
        self.assertIn(
            call().add_column("ISIN", justify="center"), table_mock.mock_calls
        )

        self.assertIn(
            call().add_row("0", "demon", "FUND", "DE00000000"), table_mock.mock_calls
        )

        console_mock.assert_called()

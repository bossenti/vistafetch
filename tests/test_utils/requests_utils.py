from http import HTTPStatus
from typing import Optional

from requests import HTTPError

EXPECTED_PRICE_DATA_CURRENCY = "EUR"
EXPECTED_PRICE_DATA_LAST = 7.09
EXPECTED_PRICE_DATA = {
                    "isoCurrency": EXPECTED_PRICE_DATA_CURRENCY,
                    "open": 7.045,
                    "low": 7.02,
                    "datetimeOpen": "2023-08-25T07:00:21.999+00:00",
                    "last": EXPECTED_PRICE_DATA_LAST,
                    "addendum": "",
                    "datetimeHigh": "2023-08-25T10:11:52.000+00:00",
                    "datetimeLow": "2023-08-25T15:07:10.000+00:00",
                    "high": 7.135,
                    "datetimeLast": "2023-08-25T15:35:10.000+00:00",
                }


def mock_api_call(*args, **kwargs):
    class MockResponse:
        def __init__(self, status_code: int, json_data: Optional[dict] = None):
            self.json_data = json_data
            self.status_code = status_code

        def raise_for_status(self):
            if self.status_code != HTTPStatus.OK:
                raise HTTPError()

        def json(self):
            return self.json_data

    if args[0].endswith("snapshot"):
        return MockResponse(
            json_data={
                "quote": EXPECTED_PRICE_DATA
            },
            status_code=200,
        )
    elif "searchValue" in args[0]:
        return MockResponse(
            json_data={
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
                    },
                    {
                        "displayType": "stock",
                        "entityType": "STOCK",
                        "isin": "DE00000000",
                        "name": "demon",
                        "symbol": "TEST",
                        "tinyName": "demon stock",
                        "wkn": "TEST00",
                    },
                ],
            },
            status_code=200,
        )

    return MockResponse(None, 404)

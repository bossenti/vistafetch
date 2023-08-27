from datetime import timezone
from unittest import TestCase

from vistafetch.model.asset import PriceData


class TestPriceData(TestCase):
    test_input = {
        "isoCurrency": "EUR",
        "open": 7.045,
        "low": 7.02,
        "datetimeOpen": "2023-08-25T07:00:21.999",
        "last": 7.09,
        "addendum": "",
        "datetimeHigh": "2023-08-25T10:11:52.000",
        "datetimeLow": "2023-08-25T15:07:10.000+00:00",
        "high": 7.135,
        "datetimeLast": "2023-08-25T15:35:10.000+00:00",
    }

    def test_datetime_validator_add_timezone(self):
        result = PriceData.model_validate(self.test_input)

        self.assertEqual(timezone.utc, result.datetime_open.tzinfo)
        self.assertEqual(timezone.utc, result.datetime_last.tzinfo)

    def test_datetime_validator_no_timestamp(self):
        test_input_malformed = self.test_input.copy()
        test_input_malformed["datetimeOpen"] = "not-a-timestamp"

        with self.assertRaises(ValueError):
            PriceData.model_validate(test_input_malformed)

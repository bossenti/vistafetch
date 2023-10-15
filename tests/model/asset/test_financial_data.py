from datetime import timezone
from unittest import TestCase

from tests.test_utils.requests_utils import EXPECTED_PRICE_DATA
from vistafetch.model.asset import PriceData


class TestPriceData(TestCase):

    def test_datetime_validator_add_timezone(self):
        result = PriceData.model_validate(EXPECTED_PRICE_DATA)

        self.assertEqual(timezone.utc, result.datetime_open.tzinfo)
        self.assertEqual(timezone.utc, result.datetime_last.tzinfo)

    def test_datetime_validator_no_timestamp(self):
        test_input_malformed = EXPECTED_PRICE_DATA
        test_input_malformed["datetimeOpen"] = "not-a-timestamp"

        with self.assertRaises(ValueError):
            PriceData.model_validate(test_input_malformed)

from unittest import TestCase

from vistafetch.model.base import VistaEntity, _snake_to_camel_case


class TestSnakeToCamelCase(TestCase):
    def test_snake_to_camel(self):
        self.assertEqual("camelCase", _snake_to_camel_case("camel_case"))
        self.assertEqual("camelCaseCase", _snake_to_camel_case("camel_case_case"))
        self.assertEqual("camel case", _snake_to_camel_case("camel case"))
        self.assertEqual("test", _snake_to_camel_case("test_"))
        self.assertEqual("test123", _snake_to_camel_case("test123"))


class TestVistaEntity(TestCase):
    test_input = {
        "test": True,
        "testCamel": "yes",
    }

    def test_as_json(self):
        result = VistaEntity.model_validate(self.test_input).as_json()

        self.assertTrue(isinstance(result, str))
        self.assertEqual("{}", result)

    def test_extra(self):
        result = VistaEntity.model_validate(self.test_input).extra
        self.assertTrue(isinstance(result, dict))
        self.assertEqual(["test", "testCamel"], list(result.keys()))
        self.assertEqual([True, "yes"], list(result.values()))

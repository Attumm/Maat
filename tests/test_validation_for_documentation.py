import os
import sys
import uuid
import unittest

from hypothesis import given
import hypothesis.strategies as st

from deepdiff import DeepDiff as ddiff

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from maat import validate

from maat import protected
from maat.exceptions import Invalid


class TestValidations(unittest.TestCase):

    def test_validation_str(self):
        """Happy path test"""
        test_input = {
            "string": "John Doe",
        }
        test_validation = {
            "string": {
                "type": "str",
                "cast": True,
                "min_length": 1,
                "max_length": 12,
                "regex": r"(\w+ )(\w+)",
                "choices": ["John Doe", "Jane Doe"],
            }   
        }
        expected = test_input.copy()

        validated_items = validate(test_input, test_validation)
        difference = ddiff(validated_items, expected)
        # if the differ finds no difference a empty dictionary is returned
        self.assertEqual(difference, {})

    def test_validation_int(self):
        """Happy path test"""
        test_input = {
            "int": 33,
        }
        test_validation = {
            "int": {
                "type": "int",
                "cast": True,
                "min_amount": 1,
                "max_amount": 150,
            }
        }
        validated_items = validate(test_input, test_validation)
        difference = ddiff(validated_items, test_input)
        # if the differ finds no difference a empty dictionary is returned
        self.assertEqual(difference, {})

    def test_validation_float(self):
        """Happy path test"""
        test_input = {
            "float": 33.0,
        }
        test_validation = {
            "float": {
                "type": "float",
                "cast": True,
                "min_amount": 1,
                "max_amount": 150,
            }
        }
        expected = test_input.copy()

        validated_items = validate(test_input, test_validation)
        difference = ddiff(validated_items, expected)
        # if the differ finds no difference a empty dictionary is returned
        self.assertEqual(difference, {})

    def test_validation_list(self):
        """Happy path test"""
        test_input = {
            "list": ["foo", "bar"],
        }
        test_validation = {
            "list": {
                "type": "list",
                "min_amount": 1,
                "max_amount": 5,
            }
        }
        expected = test_input.copy()

        validated_items = validate(test_input, test_validation)
        difference = ddiff(validated_items, expected)
        # if the differ finds no difference a empty dictionary is returned
        self.assertEqual(difference, {})

    def test_validation_dict(self):
        """Happy path test"""
        test_input = {
            "dict": {"foo": "bar", "bar": "foo"},
        }
        test_validation = {
            "dict": {
                "type": "dict",
                "min_amount": 1,
                "max_amount": 2,
                "key_regex": r"(\w+)",
            }
        }
        expected = test_input.copy()

        validated_items = validate(test_input, test_validation)
        difference = ddiff(validated_items, expected)
        # if the differ finds no difference a empty dictionary is returned
        self.assertEqual(difference, {})

    def test_validations_combined(self):
        """Copy Past this validation as starting point"""
        test_input = {
            "string": "John Doe",
            "int   ": 33,
            "float ": 33.0,
            "list  ": ["foo", "bar"],
            "dict  ": {"foo": "bar", "bar": "foo"},
        }
        test_validation = {
            "string": {"type": "str", "cast": True, "min_length": 1, "max_length": 12, "regex": r"(\w+ )(\w+)", "choices": ["John Doe", "Jane Doe"]},   
            "int   ": {"type": "int", "cast": True, "min_amount": 1, "max_amount": 150},
            "float ": {"type": "float", "cast": True, "min_amount": 1, "max_amount": 150},
            "list  ": {"type": "list", "min_amount": 1, "max_amount": 5},
            "dict  ": {"type": "dict", "min_amount": 1, "max_amount": 2, "key_regex": r"(\w+)"},
        }
        validated_items = validate(test_input, test_validation)
        expected = test_input.copy()

        difference = ddiff(validated_items, expected)
        # if the differ finds no difference a empty dictionary is returned
        self.assertEqual(difference, {})

    def test_validations_use_default(self):
        test_input = {}
        test_validation = {
            "int   ": {"type": "int", "default": 42},
        }
        expected = {
            "int   ": 42,
        }
        validated_items = validate(test_input, test_validation)
        difference = ddiff(validated_items, expected)
        # if the differ finds no difference a empty dictionary is returned
        self.assertEqual(difference, {})

    def test_validations_use_optional(self):
        test_input = {}
        test_validation = {
            "float   ": {"type": "float", "optional": True},
        }
        expected = {}
        validated_items = validate(test_input, test_validation)
        difference = ddiff(validated_items, expected)
        # if the differ finds no difference a empty dictionary is returned
        self.assertEqual(difference, {})

    def test_validations_use_nullable(self):
        test_input = {
            "str   ": None
        }
        test_validation = {
                "str   ": {"type": "str", "nullable": True},
        }
        expected = {
            "str   ": None
        }
        validated_items = validate(test_input, test_validation)
        difference = ddiff(validated_items, expected)
        # if the differ finds no difference a empty dictionary is returned
        self.assertEqual(difference, {})


    def test_validations_combined_use_nullable_optional_default(self):
        test_input = {
            "str   ": None
        }
        test_validation = {
                "int   ": {"type": "int", "min_amount": 1, "default": 42},
                "float ": {"type": "float", "optional": True},
                "str   ": {"type": "str", "nullable": True},
        }
        expected = {
            "int   ": 42,
            "str   ": None
        }
        validated_items = validate(test_input, test_validation)
        difference = ddiff(validated_items, expected)
        # if the differ finds no difference a empty dictionary is returned
        self.assertEqual(difference, {})

    def test_validations_nested(self):
        test_input = {
            "foo": {
                "foo_bar": "John Doe Street",
                "foo_baz": 123,
            }
        }
        test_validation = {
            "foo": {"type": "dict", "key_regex": r"\w+", "nested": {
                "foo_bar": {"type": "str", "min_length": 5, "max_length": 99},
                "foo_baz": {"type": "int", "min_amount": 1},
                }
            }
        }
        expected = test_input
        validated_items = validate(test_input, test_validation)
        difference = ddiff(validated_items, expected)
        # if the differ finds no difference a empty dictionary is returned
        self.assertEqual(difference, {})

    def test_validate_nested_list_dict_nested(self):
        test_input = {
            'foobar': [
                {'name': 'John Doe', 'points': 22},
                {'name': 'Jane Doe', 'points': 23},
                {'name': 'willo wanka', 'points': 42},
            ]
        }
        test_validation = {
            'foobar': {'type': 'list_dicts',  'nested': {
                    'name': {'type': 'str'},
                    'points': {'type': 'int'},
                }
            }
        }
        expected = test_input
        validated_items = validate(test_input, test_validation)
        difference = ddiff(validated_items, expected)
        # if the differ finds no difference a empty dictionary is returned
        self.assertEqual(difference, {})

if __name__ == "__main__":
    unittest.main()

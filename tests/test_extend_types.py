import os
import sys
import uuid
from datetime import datetime
import unittest

from hypothesis import given
import hypothesis.strategies as st

from deepdiff import DeepDiff as ddiff

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from maat import validate

from maat import types

from maat import protected
from maat.exceptions import Invalid


def datetime_parse(val, key, formats="%Y-%m-%dT%H:%M:%S.%f", *args, **kwargs):
    """Parse datetime string 'val' in ISO format and return a datetime object,
    raise Invalid exception on error."""
    try:
        return datetime.strptime(val, formats)
    except Exception as e:
        raise Invalid(f'key: "{key}" contains invalid item "{type(val).__name__}": unable to convert from type')


class TestExtendMaat(unittest.TestCase):

    def test_extend_maat_datetime_happy_path(self):
        """Happy path test, Maat c"""
        
        types['custom_datetime'] = datetime_parse

        test_input = {
            "created": "2022-01-28T15:01:46.0000",
        }
        test_validation = {
            "created": {
                "type": "custom_datetime",
            }   
        }
        expected = {"created": datetime(2022, 1, 28, 15, 1, 46)}

        validated_items = validate(test_input, test_validation)
        difference = ddiff(validated_items, expected)
        # if the differ finds no difference a empty dictionary is returned
        self.assertEqual(difference, {})

    def test_extend_maat_datetime_invalid_input(self):
        """Test with invalid time string, this string doens't adhere to full iso format.
        It only contains a date.
        """
        
        types['custom_datetime'] = datetime_parse

        test_input = {
            "created": "2022-01-28",
        }
        test_validation = {
            "created": {
                "type": "custom_datetime",
            }   
        }

        with self.assertRaisesRegex(Invalid, 'key: "created" contains invalid item "str": unable to convert from type'):
            _ = validate(test_input, test_validation)

    def test_extend_maat_datetime_with_argument(self):
        """Test with invalid time string, this string doens't adhere to full iso format.
        It only contains a date.
        """
        
        types['custom_datetime'] = datetime_parse

        test_input = {
            "created": "2022-01-28",
        }
        test_validation = {
            "created": {
                "type": "custom_datetime",
                "formats": "%Y-%m-%d",
            }   
        }

        expected = {"created": datetime(2022, 1, 28)}

        validated_items = validate(test_input, test_validation)
        difference = ddiff(validated_items, expected)
        # if the differ finds no difference a empty dictionary is returned
        self.assertEqual(difference, {})

    def test_extend_maat_datetime_invalid_input_int(self):
        """Test with invalid time string, this string doens't adhere to full iso format.
        It only contains a date.
        """
        
        types['custom_datetime'] = datetime_parse

        test_input = {
            "created": 161234344,
        }
        test_validation = {
            "created": {
                "type": "custom_datetime",
                "formats": "%Y-%m-%d",
            }   
        }

        with self.assertRaisesRegex(Invalid, 'key: "created" contains invalid item "int": unable to convert from type'):
            _ = validate(test_input, test_validation)

if __name__ == "__main__":
    unittest.main()

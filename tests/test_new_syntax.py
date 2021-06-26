import os
import sys
import uuid
import unittest

from deepdiff import DeepDiff as ddiff

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import maat

from maat import validate, scale
from maat.exceptions import Invalid

from maat.validations import uuid_validation
from maat.validations import int_validation, str_validation, float_validation, list_validation, dict_validation


class TestNewSyntaxValidation(unittest.TestCase):

    def setUp(self):
        self.test_input = {
            'id': 23,
            'name': 'John Doe',
            'type': 'banana',
        }
        self.test_validation = {
            #'id': {'type': 'int', 'args': {'min_amount': 1}}, old syntax for reference
            'id': {'type': 'int', 'min_amount': 1},
            #'name': {'type': 'str', 'args': {'min_length': 1, 'max_length': 35, 'regex': r'(\w+ )(\w+)'}}
            'name': {'type': 'str', 'min_length': 1, 'max_length': 35, 'regex': r'(\w+ )(\w+)'},
            #'type': {'type': 'str', 'args': {'choices': ['apple', 'banana', 'citrus']}}
            'type': {'type': 'str', 'choices': ['apple', 'banana', 'citrus']}
        }

    def test_validation(self):
        """Happy path test"""
        validated_items = scale(self.test_input, self.test_validation)
        difference = ddiff(validated_items, self.test_input)

        # if the differ finds no difference a empty dictionary is returned
        self.assertEqual(difference, {})

        validated_items = validate(self.test_input, self.test_validation)
        difference = ddiff(validated_items, self.test_input)

        # if the differ finds no difference a empty dictionary is returned
        self.assertEqual(difference, {})

    def test_validation_new_syntax_str_cast(self):
        test_input = {'id': 23}
        expected = {'id': '23'}
        counter_dict = {'id': {'type': 'str', 'cast': True}}
        result = maat.scale(test_input, counter_dict)
        self.assertEqual(expected, result)
        result = maat.validate(test_input, counter_dict)
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()

import os
import sys
import uuid
import unittest

from deepdiff import DeepDiff as ddiff

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from maat import uuid_validation
from maat import maat_scale, Invalid
from maat import int_validation, str_validation, float_validation, list_validation, dict_validation

from maat import validate_args

import maat

class TestNewSyntaxValidation(unittest.TestCase):

    def setUp(self):
        self.test_input = {
            'id': 23,
            'name': 'John Doe',
            'type': 'banana',
        }
        self.test_validation = {
            #'id': {'validator': 'int', 'args': {'min_amount': 1}}, old syntax for reference
            'id': {'validator': 'int', 'min_amount': 1},
            #'name': {'validator': 'str', 'args': {'min_length': 1, 'max_length': 35, 'regex': r'(\w+ )(\w+)'}}
            'name': {'validator': 'str', 'min_length': 1, 'max_length': 35, 'regex': r'(\w+ )(\w+)'},
            #'type': {'validator': 'str', 'args': {'choices': ['apple', 'banana', 'citrus']}}
            'type': {'validator': 'str', 'choices': ['apple', 'banana', 'citrus']}
        }

    def test_validation(self):
        """Happy path test"""
        validated_items = maat_scale(self.test_input, self.test_validation)
        difference = ddiff(validated_items, self.test_input)

        # if the differ finds no difference a empty dictionary is returned
        self.assertEqual(difference, {})

    def test_validation_new_syntax_str_cast(self):
        test_input = {'id': 23}
        expected = {'id': '23'}
        counter_dict = {'id': {'validator': 'str', 'cast': True}}
        result = maat.maat_scale(test_input, counter_dict)
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()

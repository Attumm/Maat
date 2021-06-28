import os
import sys
import uuid
import unittest

from hypothesis import given
import hypothesis.strategies as st

from deepdiff import DeepDiff as ddiff

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from maat import validate

from maat import protected
from maat.exceptions import Invalid

from maat.validations import uuid_validation
from maat.validations import int_validation, str_validation, float_validation, list_validation, dict_validation


class TestValidation(unittest.TestCase):

    def setUp(self):
        self.test_input = {
            'id': 23,
            'name': 'John Doe',
            'type': 'banana',
        }
        self.test_validation = {
            'id': {'type': 'int', 'min_amount': 1},
            'name': {'type': 'str', 'min_length': 1, 'max_length': 35, 'regex': r'(\w+ )(\w+)'},
            'type': {'type': 'str', 'choices': ['apple', 'banana', 'citrus']}
        }

    def test_validation(self):
        """Happy path test"""
        validated_items = validate(self.test_input, self.test_validation)
        difference = ddiff(validated_items, self.test_input)

        # if the differ finds no difference a empty dictionary is returned
        self.assertEqual(difference, {})

    def test_validation_test_invalid_keys_exception(self):
        """Test invalid keys exception"""

        del self.test_input['type']

        with self.assertRaisesRegex(Invalid, 'key:"type" is not set'):
            _ = validate(self.test_input, self.test_validation)

    def test_validation_test_remove_key_and_set_optional(self):
        """Test remove key and set optional"""

        del self.test_input['type']
        self.test_validation['type']['optional'] = True

        validated_items = validate(self.test_input, self.test_validation)
        difference = ddiff(validated_items, self.test_input)
        self.assertEqual(difference, {})

    def test_validation_test_remove_key_and_remove_required(self):
        """Test remove key and set optional"""

        del self.test_input['type']
        self.test_validation['type']['optional'] = True
        excepted_value = 'banana'
        self.test_validation['type']['default'] = excepted_value

        validated_items = validate(self.test_input, self.test_validation)
        difference = ddiff(validated_items, self.test_input)
        self.assertEqual(difference, {'dictionary_item_removed': set(["root['type']"])})
        self.assertEqual(validated_items['type'], excepted_value)

    def test_validation_test_remove_key_and_set_default(self):
        """Test remove key and set optional"""

        del self.test_input['type']
        excepted_value = 'banana'
        self.test_validation['type']['default'] = excepted_value

        validated_items = validate(self.test_input, self.test_validation)
        difference = ddiff(validated_items, self.test_input)
        self.assertEqual(difference, {'dictionary_item_removed': set(["root['type']"])})
        self.assertEqual(validated_items['type'], excepted_value)

    def test_validate_invalid_id(self):
        """Set id to invalid value, expect Exception"""
        self.test_input['id'] = -1

        with self.assertRaisesRegex(Invalid, 'key: "id" contains invalid item "-1": integer is less then 1'):
            _ = validate(self.test_input, self.test_validation)

    def test_validate_invalid_int_value_name(self):
        self.test_input['name'] = 30
        with self.assertRaisesRegex(Invalid, 'key: "name" contains invalid item "30" with type "int": not of type string'):
            _ = validate(self.test_input, self.test_validation)

        # test validator of name to make the previous invalid value valid.
        self.test_validation['name'] = {'type': 'int'}
        validated_items = validate(self.test_input, self.test_validation)
        difference = ddiff(validated_items, self.test_input)
        self.assertEqual(difference, {})

    def test_validate_float_value_name(self):
        self.test_input['name'] = 30.0
        with self.assertRaisesRegex(Invalid, 'key: "name" contains invalid item "30.0" with type "float": not of type string'):
            _ = validate(self.test_input, self.test_validation)

        # test validator of name to make the previous invalid value valid.
        self.test_validation['name'] = {'type': 'float'}
        validated_items = validate(self.test_input, self.test_validation)
        difference = ddiff(validated_items, self.test_input)
        self.assertEqual(difference, {})

    def test_validate_programming_error_trying_to_validate_non_dict(self):
        test_input = [1, 2, 4]
        with self.assertRaisesRegex(Invalid, "\[1, 2, 4\] not a dictionary but is of type list"):
            _ = validate(test_input, self.test_validation)

        test_input = set([1, 2, 3])
        with self.assertRaisesRegex(Invalid, "\{1, 2, 3\} not a dictionary but is of type set"):
            _ = validate(test_input, self.test_validation)

        test_input = 1
        with self.assertRaisesRegex(Invalid, "1 not a dictionary but is of type int"):
            _ = validate(test_input, self.test_validation)

        test_input = None
        with self.assertRaisesRegex(Invalid, "None not a dictionary but is of type None"):
            _ = validate(test_input, self.test_validation)

    def test_validate_nested_dict(self):
        self.test_input = {
            'id': 23,
            'addresses': {
                'street': 'John Doe Street',
                'number': 123,
            }
        }
        self.test_validation = {
            'id': {'type': 'int', 'min_amount': 1},
            'addresses': {'type': 'dict', 'key_regex': r'\w+', 'nested': {
                'street': {'type': 'str', 'min_length': 5, 'max_length': 99},
                'number': {'type': 'int', 'min_amount': 1},
                }
            }
        }
        validated_items = validate(self.test_input, self.test_validation)
        difference = ddiff(validated_items, self.test_input)
        self.assertEqual(difference, {})

    def test_validate_nested_dict_fail_on_regex(self):
        self.test_input = {
            'id': 23,
            'addresses': {
                'street': 'John Doe Street',
                'number': 123,
            }
        }
        self.test_validation = {
            'id': {'type': 'int', 'min_amount': 1},
            'addresses': {'type': 'dict', 'key_regex': r'\d+', 'nested': {
                'street': {'type': 'str', 'min_length': 5, 'max_length': 99},
                'number': {'type': 'int', 'min_amount': 1},
                }
            }
        }
        with self.assertRaisesRegex(Invalid, 'addresses: has dictionary key "street" that does not adhere to regex \\\d+'):
            _ = validate(self.test_input, self.test_validation)

    def test_validate_nested_list(self):
        self.test_input = {
            'id': 23,
            'addresses': [
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
            ]
        }
        self.test_validation = {
            'id': {'type': 'int', 'min_amount': 1},
            'addresses': {'type': 'list_dicts',  'nested': {
                    'street': {'type': 'str', 'min_length': 5, 'max_length': 99},
                }
            }
        }

        validated_items = validate(self.test_input, self.test_validation)
        difference = ddiff(validated_items, self.test_input)
        self.assertEqual(difference, {})

    def test_validate_two_deep_nested_dict(self):
        self.test_input = {
            'id': 23,
            'addresses': {
                'street': {
                    'two': 'deep',
                }
            }
        }
        self.test_validation = {
            'id': {'type': 'int', 'min_amount': 1},
            'addresses': {'type': 'dict', 'key_regex': r'\w+',
                'nested': {
                    'street': {'type': 'dict', 'min_amount': 1, 'max_length': 99,
                        'nested': {
                            'two': {'type': 'str', 'min_length': 3, 'max_length': 99},
                        }
                    }
                }
            }
        }
        validated_items = validate(self.test_input, self.test_validation)
        difference = ddiff(validated_items, self.test_input)
        self.assertEqual(difference, {})

    def test_validate_very_nested_dict(self):
        nested_dict = {
            'data': {
                'people': {
                    '7': {
                        'id': 7,
                        'name': 'John Doe',
                        'type': 'mimic',
                        'x': 823.6228647149701,
                        'y': 157.57736006592654,
                        'address': {
                            'id': 23,
                            'addresses': {
                                'street': {
                                    'two': 'deep',
                                    '222': 'deep',
                                }
                            }
                        }
                    },
                    '208': {
                        'id': 208,
                        'name': 'John Doe Too',
                        'type': 'person',
                        'x': 434.9446032612515,
                        'y': 580.0,
                        'address': {
                            'id': 23,
                            'addresses': {
                                'street': {
                                    'two': 'deep',
                                    '222': 'deep',
                                }
                            }
                        }
                    }
                },
                'streets': {
                    'id': 23,
                    'addresses': [
                        {'street': 'John Doe Street'},
                        {'street': 'John Doe Street'},
                        {'street': 'John Doe Street'},
                        {'street': 'John Doe Street'},
                    ]
                }
            }
        }
        addresses_item = {
            'id': {'type': 'int', 'min_amount': 1},
            'addresses': {'type': 'dict', 'nested': {
                'street': {'type': 'dict', 'min_amount': 1, 'max_length': 99, 'nested': {
                    'two': {'type': 'str', 'min_length': 3, 'max_length': 99},
                    '222': {'type': 'str', 'min_length': 3, 'max_length': 99},
                        }
                    }
                }
            }
        }

        geo_item = {
            'id': {'type': 'int', 'min_amount': 1},
            'name': {'type': 'str', 'min_length': 1, 'max_length': 35, 'regex': '([^\s]+)'},
            'type': {'type': 'str', 'min_length': 1, 'max_length': 25, 'regex': r'([^\s]+)'},
            'x': {'type': 'float'},
            'y': {'type': 'float'},
            'address': {'type': 'dict',
                'nested': addresses_item}
        }

        nested_dict_validation = {
            'data': {'type': 'dict', 'nested': {
                'people': {'type': 'aso_array', 'min_amount': 1, 'max_amount': 99,
                    'nested': geo_item},
                'streets': {'type': 'dict', 'nested': {
                    'id': {'type': 'int', 'min_amount': 1},
                    'addresses': {'type': 'list_dicts', 'nested': {
                        'street': {'type': 'str', 'min_length': 1, 'max_length': 99}
                                }
                            }
                        }
                    }
                }
            }
        }
        validated_items = validate(nested_dict, nested_dict_validation)
        difference = ddiff(validated_items, nested_dict)
        self.assertEqual(difference, {})


    def test_validate_very_nested_dict_fail_lowest_item(self):
        nested_dict = {
            'data': {
                'people': {
                    '7': {
                        'id': 7,
                        'name': 'John Doe',
                        'type': 'mimic',
                        'x': 823.6228647149701,
                        'y': 157.57736006592654,
                        'address': {
                            'id': 23,
                            'addresses': {
                                'street': {
                                    'two': 'deep',
                                    '222': 'deep',
                                }
                            }
                        }
                    },
                    '208': {
                        'id': 208,
                        'name': 'John Doe Too',
                        'type': 'person',
                        'x': 434.9446032612515,
                        'y': 580.0,
                        'address': {
                            'id': 23,
                            'addresses': {
                                'street': {
                                    'two': 'deep',
                                    '222': 'deep',
                                }
                            }
                        }
                    }
                },
                'streets': {
                    'id': 23,
                    'addresses': [
                        {'street': 'John Doe Street'},
                        {'street': 'John Doe Street'},
                        {'street': 'John Doe Street'},
                        {'street': 'John Doe Street'},
                    ]
                }
            }
        }
        addresses_item = {
            'id': {'type': 'int', 'min_amount': 1},
            'addresses': {'type': 'dict', 'nested': {
                'street': {'type': 'dict', 'min_amount': 1, 'max_length': 99, 'nested': {
                    'two': {'type': 'str', 'min_length': 3, 'max_length': 99},
                    '222': {'type': 'str', 'min_length': 3, 'max_length': 99, 'choices': [
                        'not_part_of_choices',
                        'fail_here']},
                        }
                    }
                }
            }
        }

        geo_item = {
            'id': {'type': 'int', 'min_amount': 1},
            'name': {'type': 'str', 'min_length': 1, 'max_length': 35, 'regex': '([^\s]+)'},
            'type': {'type': 'str', 'min_length': 1, 'max_length': 25, 'regex': r'([^\s]+)'},
            'x': {'type': 'float'},
            'y': {'type': 'float'},
            'address': {'type': 'dict',
                'nested': addresses_item}
        }

        nested_dict_validation = {
            'data': {'type': 'dict', 'nested': {
                'people': {'type': 'aso_array', 'min_amount': 1, 'max_amount': 99,
                    'nested': geo_item},
                'streets': {'type': 'dict', 'nested': {
                    'id': {'type': 'int', 'min_amount': 1},
                    'addresses': {'type': 'dict', 'nested': {
                        'street': {'type': 'str', 'min_length': 1, 'max_length': 99}
                                }
                            }
                        }
                    }
                }
            }
        }
        exp_exc_msg = "key: \"222\" contains invalid item \"deep\": not in valid choices \['not_part_of_choices', 'fail_here'\]"
        with self.assertRaisesRegex(Invalid, exp_exc_msg):
            _ = validate(nested_dict, nested_dict_validation)

    def test_validate_item_200_deep(self):
        """Lower depth for deepdiff limits, then later tests"""
        input_dict = current = {}
        counter_dict = counter_current = {}

        times = 200
        for _ in range(times):
            current['nested_dic'] = {}
            current = current['nested_dic']

        # set last item
        current['last'] = 4

        counter_current['nested_dic'] = {'type': 'dict', 'min_amount': 0, 'max_amount': 10, 'nested': {}}
        for _ in range(times - 1):
            counter_current['nested_dic']['nested'] = {'nested_dic': {'type': 'dict', 'min_amount': 0, 'max_amount': 10, 'nested': {}}}
            counter_current = counter_current['nested_dic']['nested']

        counter_current['nested_dic']['nested'] = {'last': {'type': 'int', 'min_amount': 1, 'max_amount': 10}}

        validated_items = validate(input_dict, counter_dict)
        difference = ddiff(validated_items, input_dict)
        self.assertEqual(difference, {})

    def test_validate_item_800_deep_invalid_item(self):
        input_dict = current = {}
        counter_dict = counter_current = {}

        times = 800
        for _ in range(times):
            current['nested_dic'] = {}
            current = current['nested_dic']

        # set last item
        current['last'] = 4

        counter_current['nested_dic'] = {'type': 'dict', 'min_amount': 0, 'max_amount': 10, 'nested': {}}
        for _ in range(times - 1):
            counter_current['nested_dic']['nested'] = {'nested_dic': {'type': 'dict', 'min_amount': 0, 'max_amount': 10, 'nested': {}}}
            counter_current = counter_current['nested_dic']['nested']

        # increase minimal amount to 5
        counter_current['nested_dic']['nested'] = {'last': {'type': 'int', 'min_amount': 5, 'max_amount': 10}}

        with self.assertRaisesRegex(Invalid, 'key: "last" contains invalid item "4": integer is less then 5'):
            _ = validate(input_dict, counter_dict)


class TestValidatorPropertyBased(unittest.TestCase):

    def result_as_bool(self, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
        except Invalid:
            return False

        return True

    @given(val=st.text(), min_length=st.integers(), max_length=st.integers())
    def test_string_size_validation_test(self, val, min_length, max_length):
        expected = (max_length +1) > len(val) > (min_length -1)
        result = self.result_as_bool(str_validation, val=val, min_length=min_length, max_length=max_length)
        self.assertEqual(expected, result)

    @given(val=st.integers(), min_amount=st.integers(),
           max_amount=st.integers())
    def test_int_validation_min_max(self, val, min_amount, max_amount):
        expected = val <= max_amount and val >= min_amount
        result = self.result_as_bool(int_validation, val=val, min_amount=min_amount, max_amount=max_amount)

        self.assertEqual(expected, result)

    #TODO Python long ints to float conversion goes wrong, thus all tests too.
    @given(val=st.floats(), min_amount=st.integers(), max_amount=st.integers())
    def test_float_validation_min_max(self, val, min_amount, max_amount):
        expected = (val <= max_amount and val >= min_amount) or (val == max_amount and min_amount == max_amount)
        result = self.result_as_bool(float_validation, val=val, min_amount=min_amount, max_amount=max_amount)
        self.assertEqual(expected, result)


class ValidatorTests(unittest.TestCase):

    def test_str_validation_untouched_test(self):
        expected = 'banana'
        result = str_validation(val=expected)
        self.assertEqual(expected, result)

    def test_str_validation_min_length(self):
        expected = '1234'
        result = str_validation(val=expected, min_length=4)
        self.assertEqual(expected, result)

    def test_str_validation_min_length_failed(self):
        expected = '123'
        with self.assertRaises(Invalid):
            _ = str_validation(val=expected, min_length=4)

    def test_validation_max_length(self):
        expected = '1234'
        result = str_validation(val=expected, max_length=4)
        self.assertEqual(expected, result)

    def test_str_validation_max_length_failed(self):
        expected = '12345'
        with self.assertRaises(Invalid):
            _ = str_validation(val=expected, max_length=4)

    def test_str_validation_reqex_test(self):
        """Match only two words with regex"""
        regex = r'^(\w+ )(\w+)$'
        expected = 'apple tree'
        result = str_validation(val=expected, regex=regex)
        self.assertEqual(expected, result)

    def test_str_validation_failed_regex_test(self):
        """Match only two words with regex"""
        regex = r'^(\w+ )(\w+)$'
        expected = 'apple tree barks what is '
        with self.assertRaises(Invalid):
            _ = str_validation(key=None, val=expected, regex=regex)

    def test_str_validation_choices_test(self):
        expected = ['apple', 'banana', 'citrus']
        for item in expected:
            result = str_validation(val=item, choices=expected)
            self.assertEqual(item, result)

    def test_str_validation_choices_wrong_item_test(self):
        choices = ['apple', 'banana', 'citrus']
        wrong_choices = ['star', 'moon']
        for item in wrong_choices:
            with self.assertRaises(Invalid):
                _ = str_validation(val=item, choices=choices)

    def test_int_validation_convert_to_int_test(self):
        expected = '5'
        with self.assertRaises(Invalid):
            _ = int_validation(val=expected)

        result = int_validation(val=expected, cast=True)
        self.assertEqual(int(expected), result)

    def test_int_validation_convert_fail_test(self):
        expected = 'appel'
        with self.assertRaises(Invalid):
            _ = int_validation(val=expected)

        with self.assertRaises(Invalid):
            _ = int_validation(val=expected, cast=True)

    def test_float_validation_convert_to_float_test(self):
        expected = '5'
        with self.assertRaises(Invalid):
            _ = float_validation(val=expected)

        result = float_validation(val=expected, cast=True)
        self.assertEqual(float(expected), result)

    def test_float_validation_convert_fail_test(self):
        expected = 'appel'
        with self.assertRaises(Invalid):
            _ = float_validation(val=expected)

        with self.assertRaises(Invalid):
            _ = float_validation(val=expected, cast=True)

    def test_list_validation_invalid_val_test(self):
        non_list_types = ['str', 2, {}, tuple(), float()]
        for item in non_list_types:
            with self.assertRaises(Invalid):
                _ = list_validation(val=item)

    def test_list_validation_invalid_too_long_test(self):
        too_long = [1, 2, 3, 4, 5]
        with self.assertRaises(Invalid):
            _ = list_validation(val=too_long, max_amount=4)

    def test_list_validation_invalid_too_short_test(self):
        too_short = [1, 2, 3, 4, 5]
        with self.assertRaises(Invalid):
            _ = list_validation(val=too_short, min_amount=6)

    def test_dict_validation_invalid_val_test(self):
        non_dict_types = ['str', 2, [], tuple(), float()]
        for item in non_dict_types:
            with self.assertRaises(Invalid):
                _ = dict_validation(val=item)

    def test_dict_validation_invalid_too_long_test(self):
        too_long = {i: i for i in range(5)}
        with self.assertRaises(Invalid):
            _ = dict_validation(val=too_long, max_amount=4)

    def test_dict_validation_invalid_too_short_test(self):
        too_short = {i: i for i in range(5)}
        with self.assertRaises(Invalid):
            _ = dict_validation(val=too_short, min_amount=6)

    def test_dict_validation_valid_regex_test(self):
        dict_with_valid_keys = {str(i): i for i in range(5)}
        result = dict_validation(val=dict_with_valid_keys, key_regex='[0-9]')
        difference = ddiff(dict_with_valid_keys, result)
        self.assertEqual(difference, {})

    def test_dict_validation_invalid_regex_test(self):
        dict_with_invalid_keys = {str(i): i for i in range(5)}
        dict_with_invalid_keys['a'] = 'not valid'
        with self.assertRaises(Invalid):
            _ = dict_validation(val=dict_with_invalid_keys, key_regex='[0-9]')

    def test_dict_validation_invalid_types_regex_test(self):
        dict_with_invalid_keys = {
            'keys': None,
            None: None,
            1: None,
        }
        with self.assertRaises(Invalid):
            _ = dict_validation(val=dict_with_invalid_keys, key_regex='[0-9]')

    def test_uuid_validation_valid_uuids(self):
        for _ in range(10):
            expected = str(uuid.uuid4())
            result = uuid_validation(val=expected)
            self.assertEqual(expected, result)

    def test_uuid_validation_invalid_uuids(self):
        none_uuids = [
            str(uuid.uuid4()) + 'a',
            'appels',
            '92ue92ueof-03i903ir039-034i309',
            None,
            [],
            {},
        ]
        for item in none_uuids:
            with self.assertRaises(Invalid):
                _ = uuid_validation(val=item)

class ValidatorWrongInputTests(unittest.TestCase):
    def setUp(self):
        self.test_input = {
            'id': 23,
            'name': 'John Doe',
            'type': 'banana',
        }
        self.test_validation = {
            'id': {'type': 'int', 'min_amount': 1},
            'name': {'type': 'str', 'min_length': 1, 'max_length': 35, 'regex': r'(\w+ )(\w+)'},
            'type': {'type': 'str', 'choices': ['apple', 'banana', 'citrus']}
        }

    def test_missing_key_validation(self):
        """Items that will raise an exception"""
        del(self.test_validation['name'])

        expected_expection_msg = 'invalid keys: name :expected keys: id, type'
        if sys.version_info[1] < 6:
            expected_expection_msg = 'invalid keys: name'

        with self.assertRaisesRegex(Invalid, expected_expection_msg):
            _ = validate(self.test_input, self.test_validation)


    def test_wrong_key_validation(self):
        """Items that will raise an exception"""
        self.test_validation['user'] = self.test_validation['name']
        del(self.test_validation['name'])

        expected_expection_msg = 'invalid keys: name :expected keys: id, type, user'
        if sys.version_info[1] < 6:
            expected_expection_msg = 'invalid keys: name'

        with self.assertRaisesRegex(Invalid, expected_expection_msg):
            _ = validate(self.test_input, self.test_validation)

    def test_missing_input_key_validation(self):
        """Items that will raise an exception"""
        del(self.test_input['id'])

        with self.assertRaisesRegex(Invalid, 'key:"id" is not set'):
            _ = validate(self.test_input, self.test_validation)

    def test_not_set_type(self):
        """Approriate message shown when trying to use a type that is not registered"""
        test_input = {'id': 23}
        test_validation = {'id': {'type': 'integer'}}

        with self.assertRaisesRegex(Invalid, 'integer is not registered as type'):
            _ = validate(test_input, test_validation)

    def test_not_set_type_nested(self):
        """Approriate message shown when trying to use a type that is not registered"""
        from maat import types
        types['newtype'] = lambda a: a

        test_input = {'id': 23}
        test_validation = {'id': {'type': 'newtype', 'nested': {'type': 'int'}}}

        with self.assertRaisesRegex(Invalid, "type newtype can't handle nested structures, use aso_array, list_dicts, dict instead"):
            _ = validate(test_input, test_validation)
        del types['newtype']

    def test_item_nullable(self):
        test_input = {'id': None}
        test_validation = {'id': {'type': 'float'}}
        with self.assertRaisesRegex(Invalid, 'key: \"id\" contains invalid item \"None\" with type \"NoneType\": not of type float'):
            _ = validate(test_input, test_validation)

        test_validation = {'id': {'type': 'float', 'nullable': True}}
        validated_items = validate(test_input, test_validation)
        difference = ddiff(validated_items, test_input)
        self.assertEqual(difference, {})


    def test_validate_skip_instead_of_fail_within_nested_list_with_custom_validation(self):
        from maat import types
        def denylist_address(val, key, *args, **kwargs):
            """Since this is a example denylisted is hardcoded.
            It could come from config or an key value store at runtime
            Either within this function or given as argument.
            """
            denylist = ['denylisted', 'deny_listed', 'DENYLISTED']
            if val in denylist:
                raise Invalid('{0} is in denylist of {1}'.format(key, val))
            return val

        types['valid_address'] = denylist_address
        test_input = {
            'id': 23,
            'addresses': [
                'denylisted',
                'valid adress',
                'also valid address',
                'deny_listed',
                'valid again',
                'DENYLISTED',
            ]
        }
        test_validation = {
            'id': {'type': 'int', 'min_amount': 1},
            'addresses': {'type': 'list', 'skip_failed': True, 'nested': {
                'type': 'valid_address'
                }
            }
        }
        expected_result = {
            'id': 23,
            'addresses': [
                'valid adress',
                'also valid address',
                'valid again',
            ]
        }
        validated_items = validate(test_input, test_validation)
        difference = ddiff(validated_items, expected_result)
        self.assertEqual(difference, {})

    def test_validate_custom_validation_context_list_type_is_not_set(self):
        test_input = {
            'id': 23,
            'addresses': [
                'denylisted',
                'valid adress',
                'also valid address',
                'deny_listed',
                'valid again',
                'DENYLISTED',
            ]
        }
        test_validation = {
            'id': {'type': 'int', 'min_amount': 1},
            'addresses': {'type': 'list', 'nested': {
                'type': 'not_registered'
                }
            }
        }

        with self.assertRaisesRegex(Invalid, 'not_registered is not registered as type'):
            _ = validate(test_input, test_validation)

    def test_validate_fail_within_nested_list_with_custom_validation(self):
        from maat import types
        def denylist_address(val, key, *args, **kwargs):
            """Since this is a example denylisted is hardcoded.
            It could come from config or an key value store at runtime
            Either within this function or given as argument.
            """
            denylist = ['denylisted', 'deny_listed', 'DENYLISTED']
            if val in denylist:
                raise Invalid('{0} is in denylist of {1}'.format(key, val))
            return val

        types['valid_address'] = denylist_address
        test_input = {
            'id': 23,
            'addresses': [
                'valid adress',
                'denylisted',
            ]
        }
        test_validation = {
            'id': {'type': 'int', 'min_amount': 1},
            'addresses': {'type': 'list', 'nested': {
                'type': 'valid_address'
                }
            }
        }
        with self.assertRaisesRegex(Invalid, "addresses is in denylist of denylisted"):
            _ = validate(test_input, test_validation)

    def test_validate_fail_within_nested_list_dicts_with_custom_validation(self):
        from maat import types
        def denylist_address(val, key, *args, **kwargs):
            """Since this is a example denylisted is hardcoded.
            It could come from config or an key value store at runtime
            Either within this function or given as argument.
            """
            denylist = ['denylisted', 'deny_listed', 'DENYLISTED']
            if val in denylist:
                raise Invalid('{0} is in denylist of {1}'.format(key, val))
            return val

        types['valid_address'] = denylist_address
        test_input = {
            'id': 23,
            'addresses': [
                {'street': 'valid adress'},
                {'street': 'denylisted'},
            ]
        }
        test_validation = {
            'id': {'type': 'int', 'min_amount': 1},
            'addresses': {'type': 'list_dicts', 'nested': {
              'street': {'type': 'valid_address'}}
            }
        }
        with self.assertRaisesRegex(Invalid, "street is in denylist of denylisted"):
            _ = validate(test_input, test_validation)

class TestValidationDecorator(unittest.TestCase):

    def setUp(self):
        self.test_input = {
            'number': 23,
            'name': 'John Doe',
            'kind': 'banana',
        }
        self.test_validation = {
            'number': {'type': 'int', 'min_amount': 1},
            'name': {'type': 'str', 'min_length': 1, 'max_length': 35, 'regex': r'(\w+ )(\w+)'},
            'kind': {'type': 'str', 'choices': ['apple', 'banana', 'citrus']}
        }

    def test_validation_of_arguments(self):
        """Happy path test"""
        @protected(self.test_validation)
        def foo(number, name, kind):
            return locals()
        result = foo(**self.test_input)
        difference = ddiff(result, self.test_input)

        # if the differ finds no difference a empty dictionary is returned
        self.assertEqual(difference, {})

    def test_validation_of_arguments_diffirent_input(self):

        @protected(self.test_validation)
        def foo(number, name, kind):
            return locals()

        number = self.test_input['number']
        name = self.test_input['name']
        kind = self.test_input['kind']

        # all arguments are part of kwargs
        result = foo(number=number, name=name, kind=kind)
        difference = ddiff(result, self.test_input)
        self.assertEqual(difference, {})

        # all arguments all part of args
        result = foo(number, name, kind)
        difference = ddiff(result, self.test_input)
        self.assertEqual(difference, {})

        # mixed arg, kwargs arguments
        result = foo(number, name, kind=kind)
        difference = ddiff(result, self.test_input)
        self.assertEqual(difference, {})

    def test_validation_of_argument_fail(self):
        """Test with validation failures"""

        @protected(self.test_validation)
        def foo(number, name, kind):
            return locals()

        # change type of number from int to str
        with self.assertRaisesRegex(Invalid, 'key: "number" contains invalid item "2" with type "str": not of type int'):
            result = foo(number='2', name='foo bar', kind='apple')

        # let's remove an argument
        with self.assertRaisesRegex(Invalid, 'key:"kind" is not set'):
            result = foo(number=2, name='foo bar')

        # tests that functions still works
        result = foo(**self.test_input)
        difference = ddiff(result, self.test_input)

        self.assertEqual(difference, {})

    def test_validation_of_argument_fail_returns_none(self):
        """Test with validation failures handle them and return None"""

        @protected(self.test_validation, fail_is_none=True)
        def foo(number, name, kind):
            return locals()

        # change type of number from int to str
        result = foo(number='2', name='foo bar', kind='apple')
        self.assertEqual(result, None)
        # let's remove an argument
        result = foo(number=2, name='foo bar')
        self.assertEqual(result, None)

        # tests that functions still works
        result = foo(**self.test_input)
        difference = ddiff(result, self.test_input)

        self.assertEqual(difference, {})

    def test_validation_of_argument_fail_with_custom_exception(self):
        """Test with validation failures raises an custom exception"""

        @protected(self.test_validation, custom_exception=KeyError)
        def foo(number, name, kind):
            return locals()

        # change type of number from int to str
        with self.assertRaisesRegex(KeyError, ''):
            result = foo(number='2', name='foo bar', kind='apple')

        # let's remove an argument
        with self.assertRaisesRegex(KeyError, ''):
            result = foo(number=2, name='foo bar')

        # tests that functions still works
        result = foo(**self.test_input)
        difference = ddiff(result, self.test_input)

        self.assertEqual(difference, {})


if __name__ == '__main__':
    unittest.main()

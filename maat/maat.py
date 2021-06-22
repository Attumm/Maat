import re
import sys
import json
import math

from uuid import UUID
from datetime import datetime


config = {
    'depth_limit': (sys.getrecursionlimit() - 50)
    }

special_arguments = ['nested', 'list', 'aso_array', 'skip_failed', 'null_able', 'optional', 'default_value', 'validator', 'pre_transform', 'transform', 'list_dicts', 'empty_list']

class Invalid(Exception):
    pass


def str_validation(val, key=None, min_length=None, max_length=None, regex=None, choices=None, cast=None):
    if cast:
        try:
            val = str(val)
        except (ValueError, TypeError):
            raise Invalid('key: "{0}" contains invalid item "{1}": unable to convert from type "{2}" to str'.format(key, type(val).__name__, val))

    if not isinstance(val, str):
        raise Invalid('key: "{0}" contains invalid item "{1}" with type "{2}": not of type string'.format(key, val, type(val).__name__))

    if min_length is not None and len(val) < min_length:
        raise Invalid('key: "{0}" contains invalid item "{1}": less then minimal length of {2}'.format(key, val, min_length))

    if max_length is not None and len(val) > max_length:
        raise Invalid('key: "{0}" contains invalid item "{1}": more then maximal length of {2}'.format(key, val, max_length))

    if regex is not None and not bool(re.match(regex, val)):
        raise Invalid('key: "{0}" contains invalid item "{1}": does not adhere to regex rules {2}'.format(key, val, regex))

    if choices is not None and val not in choices:
        raise Invalid('key: "{0}" contains invalid item "{1}": not in valid choices {2}'.format(key, val, choices))

    return val


def int_validation(val, key=None, min_amount=None, max_amount=None, cast=None):
    if cast:
        try:
            val = int(val)
        except (ValueError, TypeError):
            raise Invalid('key: "{0}" contains invalid item "{1}": unable to convert from type "{2}" to integer'.format(key, type(val).__name__, val))

    if not isinstance(val, int):
        raise Invalid('key: "{0}" contains invalid item "{1}" with type "{2}": not of type int'.format(key, val, type(val).__name__))

    if min_amount is not None and val < min_amount:
        raise Invalid('key: "{0}" contains invalid item "{1}": integer is less then {2}'.format(key, val, min_amount))

    if max_amount is not None and val > max_amount:
        raise Invalid('key: "{0}" contains invalid item "{1}": integer is less then {2}'.format(key, val, max_amount))

    return val


def float_validation(val, key=None, min_amount=None, max_amount=None, cast=None):
    if cast:
        try:
            val = float(val)
        except (ValueError, TypeError):
            raise Invalid('key: "{0}" contains invalid item "{1}": unable to convert from type "{2}" to float'.format(key, type(val).__name__, val))

    if not isinstance(val, float) or math.isnan(val):
        raise Invalid('key: "{0}" contains invalid item "{1}" with type "{2}": not of type float'.format(key, val, type(val).__name__))

    if min_amount is not None and val < min_amount:
        raise Invalid('key: "{0}" contains invalid item "{1}": float is less then {2}'.format(key, val, min_amount))

    if max_amount is not None and val > max_amount:
        raise Invalid('key: "{0}" contains invalid item "{1}": float is less then {2}'.format(key, val, max_amount))

    return val


def list_validation(val, key=None, min_amount=None, max_amount=None):
    if not isinstance(val, list):
        raise Invalid('key: "{0}" contains invalid item "{1}" with type "{2}": not of type list'.format(key, val, type(val).__name__))

    if min_amount is not None and len(val) < min_amount:
        raise Invalid('key: "{0}" contains invalid item "{1}": contains less then minimal amount of {2}'.format(key, val, min_amount))

    if max_amount is not None and len(val) > max_amount:
        raise Invalid('{0} contains invalid item {1}: contains more then maximum amount of {2}'.format(key, val, max_amount))

    return val


def dict_validation(val, key=None, min_amount=None, max_amount=None, key_min=None, key_max=None, key_regex=None):
    if not isinstance(val, dict):
        raise Invalid('"{}": is not a dictionary'.format(key))

    if min_amount is not None and len(val) < min_amount:
        raise Invalid('key: "{0}" contains invalid item "{1}": contains less then minimal amount of {2}'.format(key, val, min_amount))

    if max_amount is not None and len(val) > max_amount:
        raise Invalid('key: "{0}" contains invalid item "{1}": contains more then maximum amount of {2}'.format(key, val, max_amount))

    if key_regex is not None and not all(bool(re.match(key_regex, str(i))) for i in val.keys()):
            raise Invalid('{0}: has dictionary key that does not adhere to regex {1}'.format(key, key_regex))

    return val


def uuid_validation(val, key=None):
    try:
        _ = UUID(val, version=4)
    except (ValueError, AttributeError, TypeError):
        raise Invalid('key: "{0}" contains invalid item "{1}": invalid UUID4'.format(key, val))

    return val


registered_functions = {
    'int': int_validation,
    'str': str_validation,
    'float': float_validation,
    'uuid': uuid_validation,
    'list': list_validation,
    'dict': dict_validation,
}

registered_transformation = {
    'int': lambda x: int(x),
    'str': lambda x: str(x),
    'float': lambda x: float(x),
    'list': lambda x: list(x),
    'json': lambda x: json.dumps(x),
    'json_dict': lambda x: json.loads(x),
}


def get_validation_func(item):
    try:
        return registered_functions[item['validator']]
    except KeyError:
        raise Invalid('{} is not registered as validator'.format(item.get('validator')))


def get_validation_args(item):
    return {k: v for k, v, in item.items() if k not in special_arguments}


def get_transformation_func(item, type_transformation):
    """Check if transformation is set. If set try to find it in registerd transformation.
    If transformation is misspelled or sit or throw an exception"""
    transformation = item.get(type_transformation)
    if transformation is None:
        return lambda x: x
    try:
        return registered_transformation[transformation]
    except KeyError:
        raise Invalid('{} is not registered as transformation'.format(transformation))


def keys_equality(input_dict, counter_dict):
    try:
        return all(k in counter_dict for k in input_dict.keys())
    except (TypeError, AttributeError):
        return False


def find_missing_keys(input_dict, counter_dict):
    try:
        found_keys = ', '.join([key for key in sorted(input_dict.keys()) if key not in counter_dict])
        return '{} :expected keys: {}'.format(found_keys, ', '.join(counter_dict.keys()))
    except (TypeError, AttributeError):
        raise Invalid('{0} not a dictionary but is of type {1}'.format(input_dict, type(input_dict).__name__))


def maat_scale(input_dict, counter_dict, counter=0):
    counter += 1
    if counter > config['depth_limit']:
        raise Invalid('{0}: invalid depth of dict'.format(counter))
        
    if not keys_equality(input_dict, counter_dict):
        raise Invalid('invalid keys: {}'.format(find_missing_keys(input_dict, counter_dict)))

    validated_items = {}
    for key, item in counter_dict.items():

        try:
            val = input_dict[key]
        except KeyError:
            if 'default_value' in item:
                validated_items[key] = item['default_value']
                continue
            elif item.get('optional'):
                continue
            else:
                raise Invalid('key:"{0}" is not set'.format(key))

        # # if the value is None, check for default value or check if it was required
        if val is None and item.get('null_able'):
            validated_items[key] = None
            continue

        validation_func = get_validation_func(item)
        validation_args = get_validation_args(item)
        pre_transformation = get_transformation_func(item, 'pre_transform')
        post_transformation = get_transformation_func(item, 'transform')

        # the validation can be done on top level, life is good
        if 'nested' not in item:
            validated_items[key] = post_transformation(validation_func(key=key, val=pre_transformation(val), **validation_args))

        elif 'list' in item:
            validated_items[key] = item.get('empty_list', []) if len(val) == 0 else []

            for nested_item in val:
                # within a list a item should be skipable
                try:
                    validated_items[key].append(post_transformation(validation_func(key=key, val=pre_transformation(nested_item), **validation_args)))
                except Invalid:
                    if not item.get('skip_failed'):
                        raise

        # the item is nested with a list of dictionary items
        elif 'list_dicts' in item:

            validation_func(key=key, val=val, **validation_args)
            for nested_item in val:
                if key not in validated_items:
                    validated_items[key] = []

                try:
                    validated_items[key].append(post_transformation(maat_scale(pre_transformation(nested_item), counter_dict[key]['nested'], counter=counter)))
                except Invalid:
                    if not item.get('skip_failed'):
                        raise

        # the item is nested. we have to start over to do the same the one level deeper
        elif not item.get('aso_array', False):
            validated_items[key] = post_transformation(maat_scale(pre_transformation(input_dict[key]), counter_dict[key]['nested'], counter=counter))

        # the item is a "associative array" dictionary e.g keys are numerical indexes
        else:
            validation_func(key=key, val=val, **validation_args)

            for nested_key, nested_val in val.items():

                # make sure dictionary is present.
                if key not in validated_items:
                    validated_items[key] = {}
                if nested_key not in validated_items[key]:
                    validated_items[key][nested_key] = {}

                validated_items[key][nested_key] = maat_scale(nested_val, counter_dict[key]['nested'], counter=counter)

    return validated_items

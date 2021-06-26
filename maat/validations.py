import re
import json
import math

from uuid import UUID

from .exceptions import Invalid

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

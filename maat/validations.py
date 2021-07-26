import re
import math

from uuid import UUID

from .exceptions import Invalid


def str_validation(val, key=None, min_length=None, max_length=None, regex=None, choices=None, cast=None, *args, **kwargs):
    if cast:
        try:
            val = str(val)
        except (ValueError, TypeError):
            raise Invalid(f'key: "{key}" contains invalid item "{type(val).__name__}": unable to convert from type  to str')

    if not isinstance(val, str):
        raise Invalid(f'key: "{key}" contains invalid item "{val}" with type "{type(val).__name__}": not of type string')

    if min_length is not None and len(val) < min_length:
        raise Invalid(f'key: "{key}" contains invalid item "{val}": less then minimal length of {min_length}')

    if max_length is not None and len(val) > max_length:
        raise Invalid(f'key: "{key}" contains invalid item "{val}": more then maximal length of {max_length}')

    if regex is not None and not bool(re.match(regex, val)):
        raise Invalid(f'key: "{key}" contains invalid item "{val}": does not adhere to regex rules {regex}')

    if choices is not None and val not in choices:
        raise Invalid(f'key: "{key}" contains invalid item "{val}": not in valid choices {choices}')

    return val


def int_validation(val, key=None, min_amount=None, max_amount=None, cast=None, *args, **kwargs):
    if cast:
        try:
            val = int(val)
        except (ValueError, TypeError):
            raise Invalid(f'key: "{key}" contains invalid item "{type(val).__name__}": unable to convert from type "{val}" to integer')

    if not isinstance(val, int):
        raise Invalid(f'key: "{key}" contains invalid item "{val}" with type "{type(val).__name__}": not of type int')

    if min_amount is not None and val < min_amount:
        raise Invalid(f'key: "{key}" contains invalid item "{val}": integer is less then {min_amount}')

    if max_amount is not None and val > max_amount:
        raise Invalid(f'key: "{key}" contains invalid item "{val}": integer is less then {max_amount}')

    return val


def float_validation(val, key=None, min_amount=None, max_amount=None, cast=None, *args, **kwargs):
    if cast:
        try:
            val = float(val)
        except (ValueError, TypeError):
            raise Invalid(f'key: "{key}" contains invalid item "{type(val).__name__}": unable to convert from type "{val}" to float')

    if not isinstance(val, float) or math.isnan(val):
        raise Invalid(f'key: "{key}" contains invalid item "{val}" with type "{type(val).__name__}": not of type float')

    if min_amount is not None and val < min_amount:
        raise Invalid(f'key: "{key}" contains invalid item "{val}": float is less then {min_amount}')

    if max_amount is not None and val > max_amount:
        raise Invalid(f'key: "{key}" contains invalid item "{val}": float is less then {max_amount}')

    return val


def list_validation(val, key=None, min_amount=None, max_amount=None, *args, **kwargs):
    if not isinstance(val, list):
        raise Invalid(f'key: "{key}" contains invalid item "{val}" with type "{type(val).__name__}": not of type list')

    if min_amount is not None and len(val) < min_amount:
        raise Invalid(f'key: "{key}" contains invalid item "{val}": contains less then minimal amount of {min_amount}')

    if max_amount is not None and len(val) > max_amount:
        raise Invalid(f'{key} contains invalid item {val}: contains more then maximum amount of {max_amount}')

    return val


def dict_validation(val, key=None, min_amount=None, max_amount=None, key_regex=None, *args, **kwargs):
    if not isinstance(val, dict):
        raise Invalid(f'"{key}": is not a dictionary')

    if min_amount is not None and len(val) < min_amount:
        raise Invalid(f'key: "{key}" contains invalid item "{val}": {len(val)} contains less then minimal amount of {min_amount}')

    if max_amount is not None and len(val) > max_amount:
        raise Invalid(f'key: "{key}" contains invalid item "{val}": {len(val)} contains more then maximum amount of {max_amount}')

    if key_regex is not None and not all(bool(re.match(key_regex, str(i))) for i in val.keys()):
        for i in val.keys():
            if not re.match(key_regex, str(i)):
                failed = str(i)
                break
        raise Invalid(f'{key}: has dictionary key "{failed}" that does not adhere to regex {key_regex}')

    return val


def uuid_validation(val, key=None, *args, **kwargs):
    try:
        _ = UUID(val, version=4)
    except (ValueError, AttributeError, TypeError):
        raise Invalid('key: "{key}" contains invalid item "{val}": invalid UUID4')

    return val


types = {
    'int': int_validation,
    'str': str_validation,
    'float': float_validation,
    'uuid': uuid_validation,
    'list': list_validation,
    'list_dicts': list_validation,
    'dict': dict_validation,
    'aso_array': dict_validation,
}

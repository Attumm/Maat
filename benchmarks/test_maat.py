import re
from datetime import datetime, timedelta, timezone

from maat import validate
from maat import Invalid, types
from maat import version

from typing import Dict, Optional, Type, Union


date_expr = r'(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})'
time_expr = (
    r'(?P<hour>\d{1,2}):(?P<minute>\d{1,2})'
    r'(?::(?P<second>\d{1,2})(?:\.(?P<microsecond>\d{1,6})\d{0,6})?)?'
    r'(?P<tzinfo>Z|[+-]\d{2}(?::?\d{2})?)?$'
)

date_re = re.compile(f'{date_expr}$')
time_re = re.compile(time_expr)
datetime_re = re.compile(f'{date_expr}[T ]{time_expr}')

EPOCH = datetime(1970, 1, 1)
MS_WATERSHED = int(2e10)
MAX_NUMBER = int(3e20)


# Custom datetime parser, Maat currently doesn't have datetime parsing.
# Scrapped this version in favor of rebuilding pydantic version for equality.
# As requested in https://github.com/samuelcolvin/pydantic/pull/1568
# def datetime_parse(val, key, formats, *args, **kwargs):
#     """ uses to parse 'formats': '%Y-%m-%dT%H:%M:%S'"""
#     try:
#         return datetime.strptime(val, formats)
#     except Exception as e:
#         raise Invalid(f'key: "{key}" contains invalid item "{type(val).__name__}": unable to convert from type')


def validate_exactly_like_pydantic(val, key, formats, *args, **kwargs):
    try:
        return datetime.fromisoformat(val)
    except ValueError:
        pass
    if val.endswith('Z'):
        try:
            return datetime.fromisoformat(val[:-1])
        except ValueError:
            raise Invalid(f'key: "{key}" contains invalid item "{type(val).__name__}": unable to convert from type')
    try:
        return -62135492638.0 <= float(val) <= 253402318800.0
    except ValueError:
        raise Invalid(f'key: "{key}" contains invalid item "{type(val).__name__}": unable to convert from type')


def get_numeric(value, native_expected_type):
    if isinstance(value, (int, float)):
        return value
    try:
        return float(value)
    except ValueError:
        return None
    except TypeError:
        raise TypeError(f'invalid type; expected {native_expected_type}, string, bytes, int or float')


def _parse_timezone(value: Optional[str], error: Type[Exception]) -> Union[None, int, timezone]:
    if value == 'Z':
        return timezone.utc
    elif value is not None:
        offset_mins = int(value[-2:]) if len(value) > 3 else 0
        offset = 60 * int(value[1:3]) + offset_mins
        if value[0] == '-':
            offset = -offset
        try:
            return timezone(timedelta(minutes=offset))
        except ValueError:
            raise error()
    else:
        return None


def from_unix_seconds(seconds: Union[int, float]) -> datetime:
    if seconds > MAX_NUMBER:
        return datetime.max
    elif seconds < -MAX_NUMBER:
        return datetime.min

    while abs(seconds) > MS_WATERSHED:
        seconds /= 1000
    dt = EPOCH + timedelta(seconds=seconds)
    return dt.replace(tzinfo=timezone.utc)


def datetime_parse(val, key, *args, **kwargs):
    if isinstance(val, datetime):
        return val

    number = get_numeric(val, 'datetime')
    if number is not None:
        return from_unix_seconds(number)

    if isinstance(val, bytes):
        val = val.decode()

    match = datetime_re.match(val)  # type: ignore
    if match is None:
        raise Invalid(f'key: "{key}" contains invalid item "{type(val).__name__}": unable to convert from type')

    kw = match.groupdict()
    if kw['microsecond']:
        kw['microsecond'] = kw['microsecond'].ljust(6, '0')

    tzinfo = _parse_timezone(kw.pop('tzinfo'), Invalid)
    kw_: Dict[str, Union[None, int, timezone]] = {k: int(v) for k, v in kw.items() if v is not None}
    kw_['tzinfo'] = tzinfo

    try:
        return datetime(**kw_)  # type: ignore
    except ValueError:
        raise Invalid(f'key: "{key}" contains invalid item "{type(val).__name__}": unable to convert from type')


# Extending Maat with datetime_parse from Pydantic
types['datetime'] = datetime_parse


class TestMaat:
    package = 'maat'
    version = version

    def __init__(self, allow_extra):
        self.schema = {
            'id': {'type': 'int'},
            'client_name': {'type': 'str', 'max_length': 255},
            'sort_index': {'type': 'float'},
            'client_phone': {'type': 'str', 'max_length': 255, 'optional': True, 'nullable': True},
            'location': {'type': 'dict', 'nested': {
                'latitude': {'type': 'float'},
                'longitude': {'type': 'float'},
                }
            },
            'contractor':  {'type': 'int', 'cast': True, 'min_amount': 1},
            'upstream_http_referrer': {'type': 'str', 'max_length': 1023, 'optional': True, 'nullable': True},
            'grecaptcha_response': {'type': 'str', 'min_length': 20, 'max_length': 1000},
            'last_updated': {'type': 'datetime'},
            'skills': {'type': 'list_dicts', 'nested': {
                'subject': {'type': 'str'},
                'subject_id': {'type': 'int'},
                'category': {'type': 'str'},
                'qual_level': {'type': 'str'},
                'qual_level_id': {'type': 'int'},
                'qual_level_ranking': {'type': 'float', 'default': 0},
                }
            }
        }

    def validate(self, data):
        try:
            return True, validate(data, self.schema)
        except Invalid as e:
            return False, str(e)

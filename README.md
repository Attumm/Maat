# Maat
[![CI](https://github.com/Attumm/Maat/actions/workflows/ci.yml/badge.svg)](https://github.com/Attumm/Maat/actions/workflows/ci.yml)
[![Downloads](https://static.pepy.tech/badge/maat/month)](https://pepy.tech/project/maat)

Maat is an easily extensible transformation and validation library for Python.
Built for corner cases and speed.

The project is named after the ancient Egyptian god [Maat](https://en.wikipedia.org/wiki/Maat).
Her scale was used to weigh the heart as described in the book of the dead.

Since Maats scale is magical, it not only validates values, it can transform them too.

Maat does dictionary-to-dictionary validation and transformation.
From those two dictionaries a new dictionary is created.
Each value of the dictionary to be validated is passed through their validation and transformation functions.

Maat doesn't use other depenencies.

## Examples

This validates that input name is of type `str` and is either "John Doe" or "Jane Doe".
Throws `Invalid` exception when validation fails. Maat has a fail fast policy.

```python
    >>> from maat import validate
    >>> user = {"name": "John Doe"}
    >>> user_validation = {"name": {"type": "str", "choices": ["John Doe", "Jane Doe"]}}
    >>> validate(user, user_validation)
    {"name": "John Doe"}
    
    >>> validate({"name": "peter pan"}, user_validation)
    Traceback (most recent call last):
    maat.validation.Invalid: key: "name" contains invalid item "peter pan": not in valid choices ["John Doe", "Jane Doe"]
    
    >>> validate({"name": 42}, user_validation)
    Traceback (most recent call last)
    maat.validation.Invalid: key: "name" contains invalid item "42" with type "int": not of type string
    
    >>>  validate({"user": "John Doe"}, user_validation)
    Traceback (most recent call last)
    maat.validation.Invalid: invalid keys: user :expected keys: name
    
    >>> validate({"name": "Jane Doe"}, user_validation)
    {"name": "Jane Doe"}

    >>> import maat
    >>> @maat.protected(user_validation)
        def create_user(name):
            return "success"

    >>> create_user("peter pan")
    Traceback (most recent call last):
    maat.maat.Invalid: key: "name" contains invalid item "peter pan": not in valid choices ["John Doe", "Jane Doe"]

    >>> create_user("John Doe")
    "success"
```

## Starting Point Example

```python
validation = {
    "int   ": {"type": "int", "cast": True, "min_amount": 1, "max_amount": 150},
    "float ": {"type": "float", "cast": True, "min_amount": 1, "max_amount": 150},
    "list  ": {"type": "list", "min_amount": 1, "max_amount": 5, "skip_failed": True},
    "dict  ": {"type": "dict", "min_amount": 1, "max_amount": 2, "key_regex": r"(\w+)"},
    "string": {"type": "str", "cast": True, "min_length": 1,
        "max_length": 12, "regex": r"(\w+ )(\w+)", "choices": ["John Doe", "Jane Doe"]
    }
}
```

#### Field Control
Each field could be nullable, optional, default; they can be added to any field.
For lists it's possible to skip failed items with skip_failed.
```python
>>> input_dic = {"str   ": None}
>>> validation = {
	"int   ": {"type": "int", "min_amount": 1, "default": 42},
	"float ": {"type": "float", "optional": True},
	"str   ": {"type": "str", "nullable": True},
}
>>> validate(input_dic, validation)
{
    "int   ": 42,
    "str   ": None
}
```
#### Nesting
Nested data structures, nested fields are treated the same as upper levels.
It's possible to nest thousand of levels, it can be increased by upping recursion level of python.
Nesting is done without any performance hit.
```python
>>> input_dic = {
    "foo": {
	"foo_bar": "John Doe Street",
	"foo_baz": 123,
    }
}
>>> validation = {
    "foo": {"type": "dict", "key_regex": r"\w+", "nested": {
	"foo_bar": {"type": "str", "min_length": 5, "max_length": 99},
	"foo_baz": {"type": "int", "min_amount": 1},
	}
    }
}
```

#### Nesting of Dicts
```python
>>> input = {
    'foobar': [
        {'name': 'John Doe', 'points': 22},
        {'name': 'Jane Doe', 'points': 23},
        {'name': 'willo wanka', 'points': 42},
    ]
}
>>> validation = {
    'foobar': {
        'type': 'list_dicts',
        'nested': {
	        'name': {'type': 'str'},
	        'points': {'type': 'int'},
	    }
    }
}
```


## Extending Maat with custom validation
```python
>>> from maat import types


>>> def datetime_parse(val, key, formats="%Y-%m-%dT%H:%M:%S.%f", *args, **kwargs):
    """ uses to parse iso format 'formats': '%Y-%m-%dT%H:%M:%S.%f'"""
    try:
        return datetime.strptime(val, formats)
    except Exception as e:
        raise Invalid(f'key: "{key}" contains invalid item')

>>> types['custom_datetime'] = datetime_parse

>>> input = {
    "created": "2022-01-28T15:01:46.0000",
}


>>> validation = {
    "created": {
        "type": "custom_datetime",
    }   
}

>>> validate(input, validation)
{'created': datetime.datetime(2022, 1, 28, 15, 1, 46)}

```


## Installation
```sh
pip install maat
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Note
This project is being used in production by multiple companies.


## Benchmark

Benchmark open-sourced from [Pydantic](https://github.com/pydantic/pydantic/tree/7f90b2f342ba338957bb8dfff3ead760edcdd9bf/benchmarks)

Package | Version | Relative Performance | Mean validation time
--- | --- | --- | ---
maat | `3.0.4` |  | 15.8μs
attrs + cattrs | `21.2.0` | 2.4x slower | 37.6μs
pydantic | `1.8.2` | 2.5x slower | 39.7μs
voluptuous | `0.12.1` | 6.2x slower | 98.6μs
marshmallow | `3.13.0` | 7.2x slower | 114.1μs
trafaret | `2.1.0` | 7.5x slower | 118.5μs
schematics | `2.1.1` | 26.6x slower | 420.9μs
django-rest-framework | `3.12.4` | 30.4x slower | 482.2μs
cerberus | `1.3.4` | 55.6x slower | 880.2μs

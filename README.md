# Maat
[![Build Status](https://travis-ci.com/Attumm/Maat.svg?branch=main)](https://travis-ci.com/Attumm/Maat)
[![Coverage Status](https://coveralls.io/repos/github/Attumm/Maat/badge.svg)](https://coveralls.io/github/Attumm/Maat)
[![Downloads](https://pepy.tech/badge/maat/week)](https://pepy.tech/project/maat)

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
    'foobar': {'type': 'list_dicts',  'nested': {
	    'name': {'type': 'str'},
	    'points': {'type': 'int'},
	}
    }
}
```

## Installation
```sh
pip install maat
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Note
This project is being used in production by multiple companies.

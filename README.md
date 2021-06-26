# Maat
[![Build Status](https://travis-ci.com/Attumm/Maat.svg?branch=main)](https://travis-ci.com/Attumm/Maat)
[![Coverage Status](https://coveralls.io/repos/github/Attumm/Maat/badge.svg)](https://coveralls.io/github/Attumm/Maat)

Maat is an easily extensible transformation and validation library for Python.
Built for corner cases.

The project is named after the ancient Egyptian god Maat.
Her scale was used to weight the heart described in the book of the dead.

Since the scale is magical besides validating values it can transform them too.

Maat does dictionary-to-dictionary validation and transformation.
from those two dictionaries a new dictionary is created.
Each value of the dictionary to be validated is passed through their validator and transformation functions.

## Examples

Validate that input name is of type `str` and is either 'John Doe' or 'Jane Doe'.
Throws `Invalid` exception when validation fails, Maat has a fail fast policy.

```python
    >>> from maat import validate
    >>> user = {'name': 'John Doe'}
    >>> user_validation = {'name': {'type': 'str', 'choices': ['John Doe', 'Jane Doe']}}
    >>> validate(user, user_validation)
    {'name': 'John Doe'}
    
    >>> validate({'name': 'peter pan'}, user_validation)
    Traceback (most recent call last):
    maat.validation.Invalid: key: "name" contains invalid item "peter pan": not in valid choices ['John Doe', 'Jane Doe']
    
    >>> validate({'name': 42}, user_validation)
    Traceback (most recent call last)
    maat.validation.Invalid: key: "name" contains invalid item "42" with type "int": not of type string
    
    >>>  validate({'user': 'John Doe'}, user_validation)
    Traceback (most recent call last)
    maat.validation.Invalid: invalid keys: user :expected keys: name
    
    >>> validate({'name': 'Jane Doe'}, user_validation)
    {'name': 'Jane Doe'}

    >>> import maat
    >>> @maat.protected(user_validation)
        def create_user(name):
            return "success"

    >>> create_user("peter pan")
    Traceback (most recent call last):
    maat.maat.Invalid: key: "name" contains invalid item "peter pan": not in valid choices ['John Doe', 'Jane Doe']

    >>> create_user("John Doe")
    'success'
```


## Authors

* **Melvin Bijman** 

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Note
This project is being used in production by multiple companies.

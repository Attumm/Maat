# Maat
[![Build Status](https://travis-ci.org/Attumm/Maat.svg?branch=master)](https://travis-ci.org/Attumm/Maat)

Maat is a easy extensible transformation and validation library for Python.
Build for corner cases.

The project is named after the ancient egyption god Maat.
Her scale was used to weight the heart described in the book of the dead.

Since the scale is magical besides validating values it can transform them too.

Maat does dictionary to dictionary validation and transformation.
from those two dictionary an new dictionary is created.
Each value of dictionary to be validated is passed through their validator and transfomation functions

## Examples

Validate that input name is of type str and is either 'John Doe' or 'Jane Doe'.
Throws Invalid exception when validation fails, Maat has a fail fast policy.

```python
    >>> import maat
    >>> user = {'name': 'John Doe'}
    >>> user_validation = {'name': {'validator': 'str', 'choices': ['John Doe', 'Jane Doe']}}
    >>> maat.scale(user, user_validation)
    {'name': 'John Doe'}
    
    >>> maat.scale({'name': 'peter pan'}, user_validation)
    Traceback (most recent call last):
    maat.validation.Invalid: key: "name" contains invalid item "peter pan": not in valid choices ['John Doe', 'Jane Doe']
    
    >>> maat.scale({'name': 42}, user_validation)
    Traceback (most recent call last)
    maat.validation.Invalid: key: "name" contains invalid item "42" with type "int": not of type string
    
    >>>  maat.scale({'user': 'John Doe'}, user_validation)
    Traceback (most recent call last)
    maat.validation.Invalid: invalid keys: user :expected keys: name
    
    >>> maat.scale({'name': 'Jane Doe'}, user_validation)
    {'name': 'Jane Doe'}
```

## Authors

* **Melvin Bijman** 

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Note
This project is being used in production by multiple companies.

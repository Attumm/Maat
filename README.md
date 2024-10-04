# Maat
[![PyPI](https://img.shields.io/pypi/v/Maat.svg)](https://pypi.org/project/Maat/)
[![CI](https://github.com/Attumm/Maat/actions/workflows/ci.yml/badge.svg)](https://github.com/Attumm/Maat/actions/workflows/ci.yml)
[![Downloads](https://static.pepy.tech/badge/maat/month)](https://pepy.tech/project/maat)
[![codecov](https://codecov.io/gh/Attumm/Maat/graph/badge.svg?token=CORUIP41EU)](https://codecov.io/gh/Attumm/Maat)




Maat is an extensible transformation and validation library for Python, designed with simplicity and readability in mind, capable of handling corner cases, nested data, and encrypted data with remarkable speed. The project is named after the ancient Egyptian god [Maat](https://en.wikipedia.org/wiki/Maat), who used a magical scale to weigh the heart as described in the Book of the Dead.

Similar to Maat's scale, this library offers dictionary-to-dictionary validation and transformation, as well as serialization by leveraging the validation schema. A new dictionary is created from two dictionaries, with each value in the dictionary to be validated passed through their respective validation and transformation functions. Maat accomplishes this without relying on external dependencies.

Maat key features:

* Simplicity and Intuitiveness: Maat's validation schema is straightforward and easy to understand, promoting maintainability and ease of use.
* Encryption and Decryption: Maat supports validation on encrypted data, helping to maintain data privacy and adhere to data protection regulations.
* Deep Nesting: The library proficiently manages nested data structures, ensuring efficient validation for complex data requirements.
* Zero Dependencies: Maat relies on no external packages for its core functionality. The packages listed in test-packages.txt are only used for testing purposes.
* Performance: Pydantic's benchmarks indicate Maat as the top-performing library among popular validation libraries.

Maat's combination of capabilities, including encryption and decryption, nesting, and exceptional performance, makes it a fitting choice for projects requiring a versatile data validation and transformation solution.

The simplicity and readability of Maat's validation schema contribute to the stability of its implementations in projects. New developers can quickly understand and work with the validation schema, making it an ideal choice for projects that value maintainability and ease of collaboration.


```python
input_dic = {
    "number": 123,
    "street": "John Doe Street",
}

validation = {
    "number": {"type": "int", "min_amount": 1},
    "street": {"type": "str", "min_length": 5, "max_length": 99},
}
```

## Examples
Maat is designed with intuitiveness and simplicity in mind, making it accessible for developers who are familiar with dictionaries. The structure of Maat's validation schema corresponds closely to the data being validated, contributing to the ease of understanding and reducing the learning curve. This example demonstrates the intuitive nature of Maat's validation schema:

This example validates that the name in the input dictionary is of type str and is either "John Doe" or "Jane Doe". Maat throws an Invalid exception when validation fails due to its fail-fast policy.

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
            return f"created user {name}"

    >>> create_user("peter pan")
    Traceback (most recent call last):
    maat.maat.Invalid: key: "name" contains invalid item "peter pan": not in valid choices ["John Doe", "Jane Doe"]

    >>> create_user("John Doe")
    "created user John Doe"
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
Nesting data structures and fields are treated as first-class citizens, allowing for seamless validation and ensuring code correctness at any level. Maat efficiently handles nesting, with minimal performance impact, and supports a vast number of nesting levels. The limit is set by Python's recursion depth, which defaults to 1k. To increase the maximum nesting depth, you can adjust Python's recursion limit via sys.setrecursionlimit().
Below is an example showcasing nesting. For example with very deep nesting [here](tests/test_corner_case.py)
```python
>>> input_dic = {
    "foo": {
        "foo_bar": "John Doe Street",
        "foo_baz": 123,
    }
}
>>> validation = {
    "foo": {
        "type": "dict",
        "key_regex": r"\w+",
        "nested": {
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


### Extending Maat with custom validation
Maat's flexibility facilitates the creation of custom validation functions tailored to specific needs. The library can be extended with new data types and validation rules according to the project requirements. In the following example, a custom validation function is implemented and integrated for datetime strings in Maat.
Additionally, creating specific types for business logic, such as "valid_address," is also possible. For a relevant example, refer to [here](tests/tests.py#L714).
```python
>>> from maat import types


>>> def datetime_parse(val, key, formats="%Y-%m-%dT%H:%M:%S.%f", *args, **kwargs):
    """Parse datetime string 'val' in ISO format and return a datetime object, raise Invalid exception on error."""
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


### Secure Validation with Encryption and Decryption

Maat enables secure validation on encrypted data, ensuring both data privacy and flexibility in the validation process. This powerful feature allows you to maintain encrypted data throughout the validation process by decrypting it only for validation purposes and re-encrypting it afterward.
##### Integration and Usage

The code snippet below illustrates the integration of encryption and decryption functions into Maat, using custom functions for encoding and decoding. These custom functions utilize AES encryption. For more information, refer to here.
Following the integration, a series of tests demonstrate the usage of Maat to validate and transform incoming data, as well as securely validate pre-encrypted data.


```python
def encode(msg_text):
    """
    Encrypts a message using AES ECB mode with right-justified padding and encodes the result in base64.

    Args:
        msg_text (str): The plaintext message to be encrypted.

    Returns:
        str: The base64-encoded encrypted message.
    """
    secret_key = os.environ.get('secret', 'veryMuchSecret').encode('utf-8')
    msg_text_bytes = msg_text.rjust(32).encode('utf-8')
    cipher = AES.new(secret_key, AES.MODE_ECB)
    encrypted_bytes = cipher.encrypt(msg_text_bytes)

    return base64.b64encode(encrypted_bytes).decode('utf-8')


def decode(encoded):
    """
    Decrypts a base64-encoded message encrypted using AES ECB mode and removes leading spaces.

    Args:
        encoded (str): The base64-encoded encrypted message.

    Returns:
        str: The decrypted message with leading spaces removed.
    """
    secret_key = os.environ.get('secret', 'veryMuchSecret').encode('utf-8')

    cipher = AES.new(secret_key, AES.MODE_ECB)
    encrypted_bytes = base64.b64decode(encoded)
    decrypted_bytes = cipher.decrypt(encrypted_bytes)
    decrypted_text = decrypted_bytes.decode('utf-8')

    return decrypted_text.lstrip()


import maat

os.environ['secret'] = 'super super secret key'.rjust(32)
maat.registered_transformation['encode'] = encode
maat.registered_transformation['decode'] = decode

# Example encode 
test_input = {
    'name': 'John Doe',
    'address': 'John Doe Street',
}
counter_dict = {
    'name': {
        'type': 'str', 'regex': 'John Doe', 'transform': 'encode'
    },
    'address': {
        'type': 'str', 'regex': 'John Doe Street', 'transform': 'encode'
    },
}

validated_items = maat.scale(test_input, counter_dict)


# Example validation on encrypted data
test_input = {
    'name': 'LcyInWDZsUv22ocRHM3+yg7QO9ArjlhP2R9v5CSZIRc=',
    'address': 'LcyInWDZsUv22ocRHM3+yryn2OYg2jesvpgClxA/sdQ=',
}

counter_dict = {
    'name': {
        'type': 'str', 'regex': 'John Doe',
        'pre_transform': 'decode', 'transform': 'encode'
    },
    'address': {
        'type': 'str', 'regex': 'John Doe Street',
        'pre_transform': 'decode', 'transform': 'encode'
    },
}
validated_items = maat.scale(test_input, counter_dict)
```


#### Benefits

This approach enables validation of encrypted data while keeping it encrypted, or performing validation and serialization on encrypted data, thereby ensuring data confidentiality and adherence to data protection regulations.


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

Maat
=========================

.. image:: https://travis-ci.org/Attumm/Maat.svg?branch=master
    :target: https://travis-ci.org/Attumm/Maat

 Maat is a easy extensible transformation and validation library for Python.
 Build for corner cases.

 The project is named after the ancient egyption god Maat.
 Her scale was used to weight the heart as described by book of the dead.

 Since the scale is magical besides validating values it can transform them too.

 Maat is an dictionary to dictionary tool, that is to say that from the input dictionary and validation dictionary
 an new dictionary is created.
 each value of dictionary to be validated is passed through their selected validator functions.
 The result is an validated new dictionary.

 Examples
 ----------------------------------

 .. code-block:: python

    >>> user = {'name': 'John Doe'}
        >>> user_validation = {'name': {'validator': 'str'}}
            >>> maat.scale(user, user_validation)
                {'name': 'John Doe'}

                More to come...

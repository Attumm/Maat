import os
import sys
import uuid
import unittest

from deepdiff import DeepDiff as ddiff

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import maat

from maat.exceptions import Invalid

from maat.validations import str_validation, float_validation, list_validation, dict_validation


class Foo(str):
    """Error once when str is called.
    Test report should not have Exception
    """

    def __init__(self):
        self.first_time = True

    def __str__(self):
        if self.first_time:
            self.first_time = False
            raise ValueError
        return "i'm foo who are you?"


class TestHandleStrCast(unittest.TestCase):

    def setUp(self):
        pass

    def test_validation(self):
        """Happy path test"""

        expected = Foo()
        result = str_validation(val=expected)
        self.assertEqual(result, expected)


    def test_validation_with_cast(self):
        
        with self.assertRaisesRegex(Invalid, 'key: "None" contains invalid item "Foo": unable to convert from type  to str'):
            str_validation(val=Foo(), cast=True)


if __name__ == '__main__':
    unittest.main()

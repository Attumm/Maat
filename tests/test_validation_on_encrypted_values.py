import os
import sys
import uuid
import unittest

from deepdiff import DeepDiff as ddiff

import base64
from Crypto.Cipher import AES


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

def encode(msg_text):
    secret_key = os.environ.get('secret', 'dontfailhere')
    cipher = AES.new(secret_key, AES.MODE_ECB) 
    return base64.b64encode(cipher.encrypt(msg_text.rjust(32))).decode('utf-8')


def decode(encoded):
    secret_key = os.environ.get('secret', 'dontfailhere')
    cipher = AES.new(secret_key,AES.MODE_ECB) 
    return cipher.decrypt(base64.b64decode(encoded)).strip().decode('utf-8')
    

import maat
os.environ['secret'] = 'super super secret key'.rjust(32)
maat.registered_transformation['encode'] = encode
maat.registered_transformation['decode'] = decode

class TestEncryptDecrypt(unittest.TestCase):
    """For eu compliance reasons data user data is stored encrypted in
    the database. Following examples take the stated above as true.
    Don't use the encryption that is used in this example in production."""
    def setUp(self):
        self.expected = {
            'name': 'John Doe',
            'address': 'John Doe Street',
        }

        self.expected_encoded = {
            'name': 'LcyInWDZsUv22ocRHM3+yg7QO9ArjlhP2R9v5CSZIRc=',
            'address': 'LcyInWDZsUv22ocRHM3+yryn2OYg2jesvpgClxA/sdQ=',
        }


    def test_validate_and_transform_incoming_data(self):
        """This test takes data, validates and then encrypt"""
        test_input = {
            'name': 'John Doe',
            'address': 'John Doe Street',
        }
        counter_dict = {
            'name': {
                'validator': 'str', 'regex': 'John Doe', 'transform': 'encode'
            },
            'address': {
                'validator': 'str', 'regex': 'John Doe Street', 'transform': 'encode'
            },
        }
        validated_items = maat.scale(test_input, counter_dict)
        difference = ddiff(validated_items, self.expected_encoded)

        # if the differ finds no difference a empty dictionary is returned
        self.assertEqual(difference, {})


    def test_decrypt_validate_and_encrypt(self):
        """This test takes encrypted data, validates and then encrypt"""
        test_input = {
            'name': 'LcyInWDZsUv22ocRHM3+yg7QO9ArjlhP2R9v5CSZIRc=',
            'address': 'LcyInWDZsUv22ocRHM3+yryn2OYg2jesvpgClxA/sdQ=',
        }

        counter_dict = {
            'name': {
                'validator': 'str', 'regex': 'John Doe',
                'pre_transform': 'decode', 'transform': 'encode'
                },
            'address': {
                'validator': 'str', 'regex': 'John Doe Street',
                'pre_transform': 'decode', 'transform': 'encode'
                },
        }
        validated_items = maat.scale(test_input, counter_dict)
        difference = ddiff(validated_items, self.expected_encoded)

        # if the differ finds no difference a empty dictionary is returned
        self.assertEqual(difference, {})


    def test_decrypt_validate_and_encrypt_fail_on_name(self):
        """This test takes encrypted data, validates and before
        encypting fails because the value of name is not valid"""
        test_input = {
            'name': 'LcyInWDZsUv22ocRHM3+yg7QO9ArjlhP2R9v5CSZIRc=',
            'address': 'LcyInWDZsUv22ocRHM3+yryn2OYg2jesvpgClxA/sdQ=',
        }

        counter_dict = {
            'name': {
                'validator': 'str', 'regex': 'Jane',
                'pre_transform': 'decode', 'transform': 'encode'
                },
            'address': {
                'validator': 'str', 'regex': 'John Doe Street',
                'pre_transform': 'decode', 'transform': 'encode'
                },
        }

        err_msg = 'key: "name" contains invalid item "John Doe": does not adhere to regex rules Jane'
        with self.assertRaisesRegex(maat.Invalid, err_msg):
            validated_items = maat.scale(test_input, counter_dict)


if __name__ == '__main__':
    unittest.main()

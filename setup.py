from os import path
from setuptools import setup

current = path.abspath(path.dirname(__file__))

with open(path.join(current, 'README.rst')) as f:
    long_description = f.read()
 
setup(
    name='Maat 2',
    author='Melvin Bijman',
    author_email='bijman.m.m@gmail.com',
    version='0.82',
    tests_requires=[
        'appdirs',
        'coverage',
        'certifi',
        'deepdiff',
        'enum34',
        'hypothesis',
        'jsonpickle',
        'packaging',
        'pyparsing',
        'pycrypto',
        'six',
        'unittest2',
        'linecache2',
        'traceback2',
        'py',
    ],
    license='MIT',

    url='https://github.com/Attumm/Maat',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)

from os import path
from setuptools import setup

current = path.abspath(path.dirname(__file__))

setup(
    name='Maat',
    author='Melvin Bijman',
    author_email='bijman.m.m@gmail.com',
    version='0.8.5',
    license='MIT',

    py_modules=['maat'],

    url='https://github.com/Attumm/Maat',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9', 
    ],
)

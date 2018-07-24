from os import path
from setuptools import setup

current = path.abspath(path.dirname(__file__))

with open(path.join(current, 'README.rst')) as f:
    long_description = f.read()
 
setup(
    name='Maat',
    author='Melvin Bijman',
    author_email='bijman.m.m@gmail.com',
    version='0.82',
    license='MIT',

    url='https://github.com/Attumm/Maat',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)

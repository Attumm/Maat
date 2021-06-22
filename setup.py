import io

from setuptools import setup

with io.open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='Maat',
    author='Melvin Bijman',
    author_email='bijman.m.m@gmail.com',
    version='0.8.6',
    license='MIT',

    py_modules=['maat'],
    packages=['maat'],

    platforms=['any'],

    description='Validate like maat',
    long_description=long_description,
    long_description_content_type='text/markdown',

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

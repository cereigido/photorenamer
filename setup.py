#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import dirname, abspath, join
from setuptools import find_packages, setup

with open(abspath(join(dirname(__file__), 'README.md'))) as fileobj:
    README = fileobj.read().strip()

setup(
    name='photorenamer',
    description='Rename your pictures to its orignal created date',
    long_description=README,
    author='Paulo Cereigido',
    url='https://github.com/cereigido/photorenamer',
    version='1.1.0',
    zip_safe=False,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'photorenamer = photorenamer:main'
        ],
    },
    packages=find_packages(),
    install_requires=[
        'pyexif==0.2.1',
        'Pillow>=2.5.3',
    ],
)

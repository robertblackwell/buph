# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='buph',
    version='0.3.0',
    description='Backup Blackwells LR Photo collection',
    long_description=readme,
    author='Rob Blackwell',
    author_email='rob@whiteacorn.com',
    url='https://github.com/robertblackwell/buph',
    license=license,
    packages=['buph'],
    entry_points={
        "console_scripts": ['buph = buph.main:main']
    },
)


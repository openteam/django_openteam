#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='openteam',
    description=("Collection of useful methods and utilities for django developing",),
    author='Egor V. Nazarkin',
    author_email='nimnull@gmail.com',
    license='BSD',
    version='0.1.0',
    py_modules=['openteam'],
    packages=find_packages(),
)

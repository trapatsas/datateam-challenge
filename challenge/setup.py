# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='challenge',
    version='0.1.0',
    description='Travel Audience Data Engineer Challenge',
    long_description=readme,
    author='Panayotis Trapatsas',
    author_email='trapatsas@gmail.com',
    url='https://www.linkedin.com/in/trapatsas',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)


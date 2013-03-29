#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup

# get version from package
import os
here = os.path.dirname(__file__)
version_file = os.path.join(here, 'src/iptools/__init__.py')
d = {}
execfile(version_file, d)
version = d['__version__']

setup(
    name = 'iptools',
    version = version,
    description = 'Python utilites for manipulating IPv4 addresses',
    long_description = "Utilities for manipulating IPv4 addresses including a class that can be used to include CIDR network blocks in Django's INTERNAL_IPS setting.",
    url = 'https://github.com/bd808/python-iptools',
    download_url = 'http://pypi.python.org/packages/source/i/iptools/',
    author = 'Bryan Davis',
    author_email = 'bd808@bd808.com',
    license = 'BSD',
    platforms = ['any',],
    package_dir = {'': 'src'},
    packages = ['iptools'],
    include_package_data = True,
    test_suite='iptools.test_iptools',
    classifiers = [
      'Development Status :: 4 - Beta',
      'Environment :: Web Environment',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: BSD License',
      'Operating System :: OS Independent',
      'Programming Language :: Python',
      'Programming Language :: Python :: 2',
      'Programming Language :: Python :: 3',
      'Topic :: Utilities',
      'Topic :: Internet',
    ],
    zip_safe=False,
)

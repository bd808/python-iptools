#!/usr/bin/env python

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

version = '0.3'

setup(
    name = 'iptools',
    version = version,
    description = 'Python utilites for manipulating IP addresses',
    long_description = "Utilities for manipulating IP addresses including a class that can be used to include CIDR network blocks in Django's INTERNAL_IPS setting.",
    url = 'http://python-iptools.googlecode.com',
    download_url = '',
    author = 'Bryan Davis',
    author_email = 'casadebender+iptools@gmail.com',
    license = 'BSD',
    platforms = ['any',],
    package_dir = {'': 'src'},
    packages = find_packages('src'),
    include_package_data = True,
    classifiers = [
      'Development Status :: 3 - Alpha', 
      'Environment :: Web Environment',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: BSD License',
      'Operating System :: OS Independent',
      'Programming Language :: Python',
      'Topic :: Utilities',
      'Topic :: Internet', 
    ],
    zip_safe=False,
)

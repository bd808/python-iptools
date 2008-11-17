#!/usr/bin/env python

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

setup(
    name = 'iptools',
    description = 'Python utilited for manipulating IP addresses',
    version = '0.1',
    url = 'http://python-iptools.googlecode.com',
    author = 'Bryan Davis',
    author_email = 'casadebender+iptools@gmail.com',
    license = 'BSD',
    platforms = ['any',],
    packages = find_packages('src'),
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

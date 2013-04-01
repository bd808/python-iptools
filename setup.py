#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from iptools import __version__
from setuptools import setup, find_packages

setup_requires = []
if 'nosetests' in sys.argv[1:]:
    setup_requires.append('nose>=1.0')

setup(
    name='iptools',
    version=__version__,
    description='Python utilites for manipulating IPv4 and IPv6 addresses',
    author='Bryan Davis',
    author_email='bd808@bd808.com',
    url='https://github.com/bd808/python-iptools',
    download_url='http://pypi.python.org/packages/source/i/iptools/',
    license='BSD',
    platforms=['any', ],
    packages=find_packages(),
    include_package_data=True,
    test_suite='tests',
    setup_requires=setup_requires,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Utilities',
        'Topic :: Internet',
    ],
    long_description="""Utilities for manipulating IPv4 and IPv6 addresses
    including a class that can be used to include CIDR network blocks
    in Django's INTERNAL_IPS setting.""",
    zip_safe=False,
)

# vim: set sw=4 ts=4 sts=4 et :

python-iptools
==============

Utilities for dealing with IPv4 addresses.

A few useful functions and objects for manipulating IPv4 addresses in python.
This was all inspired by a desire to be able to use CIDR address notation to
designate INTERNAL_IPS in a [Django][] project's settings file.

Functions
---------

* `validate_ip`: Validate a dotted quad IPv4 address.
* `ip2long`: Convert a dotted quad IPv4 address to a network byte order 32-bit
  integer.
* `long2ip`: Convert a network byte order 32-bit integer to a dotted quad IPv4
  address.
* `validate_cidr`: Validate a CIDR notation IPv4 address.
* `cidr2block`: Convert a CIDR notation IPv4 address into a tuple containing
  network block start and end addresses.

Objects
-------

* `IpRange`: Range of IPv4 addresses providing `in` and iteration.
* `IpRangeList`: List of IpRange objects providing `in` and iteration.

Using with Django
-----------------

The IpRangeList object can be used in a Django settings file to allow [CIDR][]
notation and/or `(start, end)` ranges to be used in the `INTERNAL_IPS` list.

### Example: ###

    #!/usr/bin/env python
    import iptools

    INTERNAL_IPS = iptools.IpRangeList(
        '127.0.0.1',                # single ip
        '192.168/16',               # CIDR network block
        ('10.0.0.1', '10.0.0.19'),  # inclusive range
    )

Python Version Compatibility
----------------------------

This library has been tested with Python versions 2.3.5, 2.6.2, & 2.3.1 on
Ubuntu x86_64 and Python 2.6.1 & 2.6.4 on Snow Leopard.

Installing
----------

Install the latest stable version using easy_install:

    easy_install iptools

or pip:

    pip install iptools

Install the latest development version:

    svn checkout http://python-iptools.googlecode.com/svn/trunk/ python-iptools
    cd python-iptools
    python setup.py install

---
[CIDR]: http://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing
[Django]: http://www.djangoproject.com/


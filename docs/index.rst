==============================
iptools - IP Address Utilities
==============================

Utilities for dealing with IPv4 addresses.

  :Functions:
    - :func:`cidr2block`: Convert a CIDR notation ip address into a tuple
      containing network block start and end addresses.
    - :func:`hex2ip`: Convert a hex encoded network byte order 32-bit
      integer to a dotted-quad ip address.
    - :func:`ip2hex`: Convert a dotted-quad ip address to a hex encoded
      network byte order 32-bit integer.
    - :func:`ip2long`: Convert a dotted-quad ip address to a network byte
      order 32-bit integer.
    - :func:`ip2network`: Convert a dotted-quad ip to base network number.
    - :func:`long2ip`: Convert a network byte order 32-bit integer to
      a dotted quad ip address.
    - :func:`netmask2prefix`: Convert a dotted-quad netmask into a CIDR
      prefix.
    - :func:`subnet2block`: Convert a dotted-quad ip address including
      a netmask into a tuple containing the network block start and end
      addresses.
    - :func:`validate_cidr`: Validate a CIDR notation ip address.
    - :func:`validate_ip`: Validate a dotted-quad ip address.
    - :func:`validate_netmask`: Validate that a dotted-quad ip address is
      a valid netmask.
    - :func:`validate_subnet`: Validate a dotted-quad ip address including
      a netmask.

  :Objects:
    - :class:`IpRange`: Range of ip addresses supporting ``in`` and iteration.
    - :class:`IpRangeList`: List of IpRange objects supporting ``in`` and
      iteration.

  :Constants:
    - :mod:`iptools.constants`: Common and special use IPv4 address blocks.

  The :class:`IpRangeList` object can be used in a django settings file to
  allow CIDR notation and/or (start, end) ranges to be used in the
  INTERNAL_IPS list.

  **Example**::

    INTERNAL_IPS = IpRangeList(
        '127.0.0.1',
        '192.168/16',
        ('10.0.0.1', '10.0.0.19'),
        )

.. automodule:: iptools
   :members:
   :exclude-members: IpRange, IpRangeList

IpRange
=======
.. autoclass:: IpRange
  :members:
  :special-members:

IpRangeList
===========
.. autoclass:: IpRangeList
  :members:
  :special-members:

Constants
=========
.. automodule:: iptools.constants
  :members:

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

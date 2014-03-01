##############################
iptools - IP Address Utilities
##############################
The iptools_ package is a collection of utilities for dealing with IP
addresses.

The project was inspired by a desire to be able to use CIDR_ address notation
to designate ``INTERNAL_IPS`` in a Django_ project's settings file.


******************************
Using with Django INTERNAL_IPS
******************************
An :class:`iptools.IpRangeList` object can be used in a Django_ settings file
to allow CIDR_ and/or ``(start, end)`` ranges to be used in the
``INTERNAL_IPS`` list.

There are many internal and add-on components for Django_ that use the
INTERNAL_IPS_ configuration setting to alter application behavior or make
debugging easier. When you are developing and testing an application by
yourself it's easy to add the ip address that your web browser will be coming
from to this list. When you are developing in a group or testing from many ips
it can become cumbersome to add more and more ip addresses to the setting
individually.

The :class:`iptools.IpRangeList` object can help by replacing the standard
tuple of addresses recommended by the Django docs with an intelligent object
that responds to the membership test operator in. This object can be
configured with dotted quad IP addresses like the default ``INTERNAL_IPS``
tuple (eg. '127.0.0.1'), CIDR_ block notation (eg. '127/8', '192.168/16') for
entire network blocks, and/or (start, end) tuples describing an arbitrary
range of IP addresses.

Django_'s internal checks against the ``INTERNAL_IPS`` tuple take the form
``if addr in INTERNAL_IPS`` or ``if addr not in INTERNAL_IPS``. This works
transparently with the :class:`iptools.IpRangeList` object because it
implements the magic method ``__contains__`` which python calls when the
``in`` or ``not in`` operators are used.

.. code-block:: python

    import iptools

    INTERNAL_IPS = iptools.IpRangeList(
        '127.0.0.1',                # single ip
        '192.168/16',               # CIDR network block
        ('10.0.0.1', '10.0.0.19'),  # arbitrary inclusive range
        '::1',                      # single IPv6 address
        'fe80::/10',                # IPv6 CIDR block
        '::ffff:172.16.0.2'         # IPv4-mapped IPv6 address
    )


****************************
Python Version Compatibility
****************************

`Travis CI`_ automatically runs tests against python 2.6, 2.7, 3.2, 3.3 and pypy.

Current test status: |build status|

************
Installation
************
Install the latest stable version from PyPi using pip_:

.. code-block:: bash

    $ pip install iptools

or setuptools_:

.. code-block:: bash

    $ easy_install iptools

Install the latest development version:

.. code-block:: bash

    $ git clone https://github.com/bd808/python-iptools.git
    $ cd python-iptools
    $ python setup.py install


***
API
***

iptools
=======
.. automodule:: iptools

iptools.IpRangeList
-------------------
.. autoclass:: iptools.IpRangeList
  :members:
  :special-members:


iptools.IpRange
---------------
.. autoclass:: iptools.IpRange
  :members:
  :special-members:


iptools.ipv4
============
.. automodule:: iptools.ipv4
  :members:


iptools.ipv6
============
.. automodule:: iptools.ipv6
  :members:


******************
Indices and tables
******************
* :ref:`genindex`
* :ref:`search`

.. _iptools: http://pypi.python.org/pypi/iptools
.. _Django: http://www.djangoproject.com/
.. _`Travis CI`: http://travis-ci.org/bd808/python-iptools
.. _pip: http://www.pip-installer.org/en/latest/
.. _setuptools: https://pypi.python.org/pypi/setuptools
.. _CIDR: http://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing
.. _INTERNAL_IPS: http://docs.djangoproject.com/en/dev/ref/settings/#internal-ips
.. |build status| image:: https://secure.travis-ci.org/bd808/python-iptools.png
   :width: 77
   :height: 19
   :alt: Build Status
   :align: middle
   :target: http://travis-ci.org/bd808/python-iptools


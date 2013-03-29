#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2008-2013, Bryan Davis
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     - Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#     - Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
"""Utilities for dealing with IPv4 addresses.

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


  The :class:`IpRangeList` object can be used in a django settings file to
  allow CIDR notation and/or (start, end) ranges to be used in the
  INTERNAL_IPS list.

  **Example**::

    INTERNAL_IPS = IpRangeList(
        '127.0.0.1',
        '192.168/16',
        ('10.0.0.1', '10.0.0.19'),
        )

"""
__version__ = '0.5.0'

__all__ = (
        'cidr2block',
        'hex2ip',
        'ip2hex',
        'ip2long',
        'ip2network',
        'long2ip',
        'netmask2prefix',
        'validate_cidr',
        'validate_ip',
        'validate_netmask',
        'validate_subnet',
        'subnet2block',
        'IpRange',
        'IpRangeList',
        )

import re

# sniff for python2.x / python3k compatibility "fixes'
try:
    basestring = basestring
except NameError:
    # 'basestring' is undefined, must be python3k
    basestring = str

try:
    next = next
except NameError:
    # builtin next function doesn't exist
    def next (iterable):
        return iterable.next()

try:
    import Sequence
except ImportError:
    # python <2.6 doesn't have abc classes to extend
    Sequence = object

try:
    bin = bin
except NameError:
    # builtin bin function doesn't exist
    def bin (x):
        """
        From http://code.activestate.com/recipes/219300/#c7
        """
        if x < 0:
            return '-' + bin(-x)
        out = []
        if x == 0:
            out.append('0')
        while x > 0:
            out.append('01'[x & 1])
            x >>= 1
            pass
        try:
            return '0b' + ''.join(reversed(out))
        except NameError:
            out.reverse()
            return '0b' + ''.join(out)
    #end bin

# end compatibility "fixes'


_DOTTED_QUAD_RE = re.compile(r'^(\d{1,3}\.){0,3}\d{1,3}$')

def validate_ip (s):
    """Validate a dotted-quad ip address.

    The string is considered a valid dotted-quad address if it consists of
    one to four octets (0-255) seperated by periods (.).


    >>> validate_ip('127.0.0.1')
    True
    >>> validate_ip('127.0')
    True
    >>> validate_ip('127.0.0.256')
    False
    >>> validate_ip(None) #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    TypeError: expected string or buffer


    :param s: String to validate as a dotted-quad ip address.
    :type s: str
    :returns: ``True`` if a valid dotted-quad ip address, ``False`` otherwise.
    :raises: TypeError
    """
    if _DOTTED_QUAD_RE.match(s):
        quads = s.split('.')
        for q in quads:
            if int(q) > 255:
                return False
        return True
    return False
#end validate_ip

_CIDR_RE = re.compile(r'^(\d{1,3}\.){0,3}\d{1,3}/\d{1,2}$')

def validate_cidr (s):
    """Validate a CIDR notation ip address.

    The string is considered a valid CIDR address if it consists of one to
    four octets (0-255) seperated by periods (.) followed by a forward slash
    (/) and a bit mask length (1-32).


    >>> validate_cidr('127.0.0.1/32')
    True
    >>> validate_cidr('127.0/8')
    True
    >>> validate_cidr('127.0.0.256/32')
    False
    >>> validate_cidr('127.0.0.0')
    False
    >>> validate_cidr(None) #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    TypeError: expected string or buffer


    :param s: String to validate as a CIDR notation ip address.
    :type s: str
    :returns: ``True`` if a valid CIDR address, ``False`` otherwise.
    :raises: TypeError
    """
    if _CIDR_RE.match(s):
        ip, mask = s.split('/')
        if validate_ip(ip):
            if int(mask) > 32:
                return False
        else:
            return False
        return True
    return False
#end validate_cidr

def validate_netmask (s):
    """Validate that a dotted-quad ip address is a valid netmask.


    >>> validate_netmask('0.0.0.0')
    True
    >>> validate_netmask('128.0.0.0')
    True
    >>> validate_netmask('255.0.0.0')
    True
    >>> validate_netmask('255.255.255.255')
    True
    >>> validate_netmask('128.0.0.1')
    False


    :param s: String to validate as a dotted-quad notation netmask.
    :type s: str
    :returns: ``True`` if a valid netmask, ``False`` otherwise.
    :raises: TypeError
    """
    if validate_ip(s):
        mask = bin(ip2network(s))[2:]
        # all left most bits must be 1, all right most must be 0
        seen0 = False
        for c in mask:
            if '1' == c:
                if seen0:
                    return False
            else:
                seen0 = True
        return True
    else:
        return False
#end validate_netmask

def validate_subnet (s):
    """Validate a dotted-quad ip address including a netmask.

    The string is considered a valid dotted-quad address with netmask if it
    consists of one to four octets (0-255) seperated by periods (.) followed
    by a forward slash (/) and a subnet bitmask which is expressed in
    dotted-quad format.


    >>> validate_subnet('127.0.0.1/255.255.255.255')
    True
    >>> validate_subnet('127.0/255.0.0.0')
    True
    >>> validate_subnet('127.0/255')
    True
    >>> validate_subnet('127.0.0.256/255.255.255.255')
    False
    >>> validate_subnet('127.0.0.1/255.255.255.256')
    False
    >>> validate_subnet('127.0.0.0')
    False
    >>> validate_subnet(None)
    Traceback (most recent call last):
        ...
    TypeError: expected string or unicode


    :param s: String to validate as a dotted-quad ip address with netmask.
    :type s: str
    :returns: ``True`` if a valid dotted-quad ip address with netmask,
        ``False`` otherwise.
    :raises: TypeError
    """
    if isinstance(s, basestring):
        if '/' in s:
            start, mask = s.split('/', 2)
            return validate_ip(start) and validate_netmask(mask)
        else:
            return False
    raise TypeError("expected string or unicode")
#end validate_subnet

def ip2long (ip):
    """Convert a dotted-quad ip address to a network byte order 32-bit
    integer.


    >>> ip2long('127.0.0.1')
    2130706433
    >>> ip2long('127.1')
    2130706433
    >>> ip2long('127')
    2130706432
    >>> ip2long('127.0.0.256') is None
    True


    :param ip: Dotted-quad ip address (eg. '127.0.0.1').
    :type ip: str
    :returns: Network byte order 32-bit integer or ``None`` if ip is invalid.
    """
    if not validate_ip(ip):
        return None
    quads = ip.split('.')
    if len(quads) == 1:
        # only a network quad
        quads = quads + [0, 0, 0]
    elif len(quads) < 4:
        # partial form, last supplied quad is host address, rest is network
        host = quads[-1:]
        quads = quads[:-1] + [0,] * (4 - len(quads)) + host

    lngip = 0
    for q in quads:
        lngip = (lngip << 8) | int(q)
    return lngip
#end ip2long

def ip2network (ip):
    """Convert a dotted-quad ip to base network number.

    This differs from :func:`ip2long` in that partial addresses as treated as
    all network instead of network plus host (eg. '127.1' expands to
    '127.1.0.0')

    :param ip: dotted-quad ip address (eg. ‘127.0.0.1’).
    :type ip: str
    :returns: Network byte order 32-bit integer or `None` if ip is invalid.
    """
    if not validate_ip(ip):
        return None
    quads = ip.split('.')
    netw = 0
    for i in range(4):
        netw = (netw << 8) | int(len(quads) > i and quads[i] or 0)
    return netw
#end ip2network

_MAX_IP = 0xffffffff
_MIN_IP = 0x0

def long2ip (l):
    """Convert a network byte order 32-bit integer to a dotted quad ip
    address.


    >>> long2ip(2130706433)
    '127.0.0.1'
    >>> long2ip(_MIN_IP)
    '0.0.0.0'
    >>> long2ip(_MAX_IP)
    '255.255.255.255'
    >>> long2ip(None) #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    TypeError: unsupported operand type(s) for >>: 'NoneType' and 'int'
    >>> long2ip(-1) #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    TypeError: expected int between 0 and 4294967295 inclusive
    >>> long2ip(374297346592387463875) #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    TypeError: expected int between 0 and 4294967295 inclusive
    >>> long2ip(_MAX_IP + 1) #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    TypeError: expected int between 0 and 4294967295 inclusive


    :param l: Network byte order 32-bit integer.
    :type l: int
    :returns: Dotted-quad ip address (eg. '127.0.0.1').
    :raises: TypeError
    """
    if _MAX_IP < l or l < 0:
        raise TypeError("expected int between 0 and %d inclusive" % _MAX_IP)
    return '%d.%d.%d.%d' % (l>>24 & 255, l>>16 & 255, l>>8 & 255, l & 255)
#end long2ip

def ip2hex (addr):
    """Convert a dotted-quad ip address to a hex encoded number.


    >>> ip2hex('0.0.0.1')
    '00000001'
    >>> ip2hex('127.0.0.1')
    '7f000001'
    >>> ip2hex('127.255.255.255')
    '7fffffff'
    >>> ip2hex('128.0.0.1')
    '80000001'
    >>> ip2hex('128.1')
    '80000001'
    >>> ip2hex('255.255.255.255')
    'ffffffff'


    :param addr: Dotted-quad ip address.
    :type addr: str
    :returns: Numeric ip address as a hex-encoded string or ``None`` if
        invalid.
    """
    netip = ip2long(addr)
    if netip is None:
        return None
    return "%08x" % netip
#end ip2hex

def hex2ip (hex_str):
    """Convert a hex encoded integer to a dotted-quad ip address.


    >>> hex2ip('00000001')
    '0.0.0.1'
    >>> hex2ip('7f000001')
    '127.0.0.1'
    >>> hex2ip('7fffffff')
    '127.255.255.255'
    >>> hex2ip('80000001')
    '128.0.0.1'
    >>> hex2ip('ffffffff')
    '255.255.255.255'


    :param hex_str: Numeric ip address as a hex-encoded string.
    :type hex_str: str
    :returns: Dotted-quad ip address or ``None`` if invalid.
    """
    try:
        netip = int(hex_str, 16)
    except ValueError:
        return None
    return long2ip(netip)
#end hex2ip

def cidr2block (cidr):
    """Convert a CIDR notation ip address into a tuple containing the network
    block start and end addresses.


    >>> cidr2block('127.0.0.1/32')
    ('127.0.0.1', '127.0.0.1')
    >>> cidr2block('127/8')
    ('127.0.0.0', '127.255.255.255')
    >>> cidr2block('127.0.1/16')
    ('127.0.0.0', '127.0.255.255')
    >>> cidr2block('127.1/24')
    ('127.1.0.0', '127.1.0.255')
    >>> cidr2block('127.0.0.3/29')
    ('127.0.0.0', '127.0.0.7')
    >>> cidr2block('127/0')
    ('0.0.0.0', '255.255.255.255')


    :param cidr: CIDR notation ip address (eg. '127.0.0.1/8').
    :type cidr: str
    :returns: Tuple of block (start, end) or ``None`` if invalid.
    :raises: TypeError
    """
    if not validate_cidr(cidr):
        return None

    ip, prefix = cidr.split('/')
    prefix = int(prefix)

    # convert dotted-quad ip to base network number
    network = ip2network(ip)

    return _block_from_ip_and_prefix(network, prefix)
#end cidr2block

def netmask2prefix (mask):
    """Convert a dotted-quad netmask into a CIDR prefix.


    >>> netmask2prefix('255.0.0.0')
    8
    >>> netmask2prefix('255.128.0.0')
    9
    >>> netmask2prefix('255.255.255.254')
    31
    >>> netmask2prefix('255.255.255.255')
    32
    >>> netmask2prefix('0.0.0.0')
    0
    >>> netmask2prefix('127.0.0.1')
    0


    :param mask: Netmask in dotted-quad notation.
    :type mask: str
    :returns: CIDR prefix corresponding to netmask or `0` if invalid.
    """
    if validate_netmask(mask):
        return bin(ip2network(mask)).count('1')
    return 0
#end netmask2prefix

def subnet2block (subnet):
    """Convert a dotted-quad ip address including a netmask into a tuple
    containing the network block start and end addresses.


    >>> subnet2block('127.0.0.1/255.255.255.255')
    ('127.0.0.1', '127.0.0.1')
    >>> subnet2block('127/255')
    ('127.0.0.0', '127.255.255.255')
    >>> subnet2block('127.0.1/255.255')
    ('127.0.0.0', '127.0.255.255')
    >>> subnet2block('127.1/255.255.255.0')
    ('127.1.0.0', '127.1.0.255')
    >>> subnet2block('127.0.0.3/255.255.255.248')
    ('127.0.0.0', '127.0.0.7')
    >>> subnet2block('127/0')
    ('0.0.0.0', '255.255.255.255')


    :param subnet: dotted-quad ip address with netmask
        (eg. '127.0.0.1/255.0.0.0').
    :type subnet: str
    :returns: Tuple of block (start, end) or ``None`` if invalid.
    :raises: TypeError
    """
    if not validate_subnet(subnet):
        return None

    ip, netmask = subnet.split('/')
    prefix = netmask2prefix(netmask)

    # convert dotted-quad ip to base network number
    network = ip2network(ip)

    return _block_from_ip_and_prefix(network, prefix)
#end subnet2block

def _block_from_ip_and_prefix (ip, prefix):
    """Create a tuple of (start, end) dotted-quad addresses from the given
    ip address and prefix length.

    :param ip: Ip address in block
    :type ip: long
    :param prefix: Prefix size for block
    :type prefix: int
    :returns: Tuple of block (start, end)
    """
    # keep left most prefix bits of ip
    shift = 32 - prefix
    block_start = ip >> shift << shift

    # expand right most 32 - prefix bits to 1
    mask = (1 << shift) - 1
    block_end = block_start | mask
    return (long2ip(block_start), long2ip(block_end))
#end _block_from_ip_and_prefix

class IpRange (Sequence):
    """
    Range of ip addresses.

    Converts a CIDR notation address, ip address and subnet, tuple of ip
    addresses or start and end addresses into a smart object which can perform
    ``in`` and ``not in`` tests and iterate all of the addresses in the range.


    >>> r = IpRange('127.0.0.1', '127.255.255.255')
    >>> '127.127.127.127' in r
    True
    >>> '10.0.0.1' in r
    False
    >>> 2130706433 in r
    True
    >>> r = IpRange('127/24')
    >>> print(r)
    ('127.0.0.0', '127.0.0.255')
    >>> r = IpRange('127/30')
    >>> for ip in r:
    ...     print(ip)
    127.0.0.0
    127.0.0.1
    127.0.0.2
    127.0.0.3
    >>> print(IpRange('127.0.0.255', '127.0.0.0'))
    ('127.0.0.0', '127.0.0.255')
    >>> r = IpRange('127/255.255.255.0')
    >>> print(r)
    ('127.0.0.0', '127.0.0.255')


    :param start: Ip address in dotted quad format, CIDR notation, subnet
        format or ``(start, end)`` tuple of ip addresses in dotted quad format.
    :type start: str or tuple
    :param end: Ip address in dotted quad format or ``None``.
    :type end: str
    """
    def __init__ (self, start, end=None):
        if end is None:
            if isinstance(start, IpRange):
                # copy constructor
                start, end = start[0], start[-1]

            elif isinstance(start, tuple):
                # occurs when IpRangeList calls via map to pass start and end
                start, end = start

            elif validate_cidr(start):
                # CIDR notation range
                start, end = cidr2block(start)

            elif validate_subnet(start):
                # Netmask notation range
                start, end = subnet2block(start)

            else:
                # degenerate range
                end = start

        start = ip2long(start)
        end = ip2long(end)
        self.startIp = min(start, end)
        self.endIp = max(start, end)
        self._len = self.endIp - self.startIp + 1
    #end __init__

    def __repr__ (self):
        """
        >>> repr(IpRange('127.0.0.1'))
        "IpRange('127.0.0.1', '127.0.0.1')"
        >>> repr(IpRange('10/8'))
        "IpRange('10.0.0.0', '10.255.255.255')"
        >>> repr(IpRange('127.0.0.255', '127.0.0.0'))
        "IpRange('127.0.0.0', '127.0.0.255')"
        """
        return "IpRange('%s', '%s')" % (
                long2ip(self.startIp), long2ip(self.endIp))
    #end __repr__

    def __str__ (self):
        """
        >>> str(IpRange('127.0.0.1'))
        "('127.0.0.1', '127.0.0.1')"
        >>> str(IpRange('10/8'))
        "('10.0.0.0', '10.255.255.255')"
        >>> str(IpRange('127.0.0.255', '127.0.0.0'))
        "('127.0.0.0', '127.0.0.255')"
        """
        return (long2ip(self.startIp), long2ip(self.endIp)).__repr__()
    #end __str__

    def __eq__ (self, other):
        """
        >>> IpRange('127.0.0.1') == IpRange('127.0.0.1')
        True
        >>> IpRange('127.0.0.1') == IpRange('127.0.0.2')
        False
        >>> IpRange('10/8') == IpRange('10', '10.255.255.255')
        True
        """
        return isinstance(other, IpRange) and \
                self.startIp == other.startIp and \
                self.endIp == other.endIp
    #end __eq__

    def __len__ (self):
        """
        Return the length of the range.


        >>> len(IpRange('127.0.0.1'))
        1
        >>> len(IpRange('127/31'))
        2
        >>> len(IpRange('127/22'))
        1024
        """
        return self._len
    #end __len__

    def __hash__ (self):
        """
        >>> a = IpRange('127.0.0.0/8')
        >>> b = IpRange('127.0.0.0', '127.255.255.255')
        >>> a.__hash__() == b.__hash__()
        True
        >>> c = IpRange('10/8')
        >>> a.__hash__() == c.__hash__()
        False
        >>> b.__hash__() == c.__hash__()
        False
        """
        return hash((self.startIp, self.endIp))
    #end __hash__

    def _cast (self, item):
        if isinstance(item, basestring):
            item = ip2long(item)
        if type(item) not in [type(1), type(_MAX_IP)]:
            raise TypeError(
                "expected dotted-quad ip address or 32-bit integer")
        return item
    #end _cast

    def index (self, item):
        """
        Return the 0-based position of `item` in this IpRange.


        >>> r = IpRange('127.0.0.1', '127.255.255.255')
        >>> r.index('127.0.0.1')
        0
        >>> r.index('127.255.255.255')
        16777214
        >>> r.index('10.0.0.1')
        Traceback (most recent call last):
            ...
        ValueError: 10.0.0.1 is not in range


        :param item: Dotted-quad ip address.
        :type item: str
        :returns: Index of ip address in range
        """
        item = self._cast(item)
        offset = item - self.startIp
        if offset >= 0 and offset < self._len:
            return offset
        raise ValueError('%s is not in range' % long2ip(item))
    #end index

    def count (self, item):
        return int(item in self)
    #end count

    def __contains__ (self, item):
        """
        Implements membership test operators ``in`` and ``not in`` for the
        address range.


        >>> r = IpRange('127.0.0.1', '127.255.255.255')
        >>> '127.127.127.127' in r
        True
        >>> '10.0.0.1' in r
        False
        >>> 2130706433 in r
        True
        >>> 'invalid' in r
        Traceback (most recent call last):
            ...
        TypeError: expected dotted-quad ip address or 32-bit integer


        :param item: Dotted-quad ip address.
        :type item: str
        :returns: ``True`` if address is in range, ``False`` otherwise.
        """
        item = self._cast(item)
        return self.startIp <= item <= self.endIp
    #end __contains__

    def __getitem__ (self, index):
        """
        >>> r = IpRange('127.0.0.1', '127.255.255.255')
        >>> r[0]
        '127.0.0.1'
        >>> r[16777214]
        '127.255.255.255'
        >>> r[-1]
        '127.255.255.255'
        >>> r[len(r)]
        Traceback (most recent call last):
            ...
        IndexError: index out of range

        >>> r[:]
        IpRange('127.0.0.1', '127.255.255.255')
        >>> r[1:]
        IpRange('127.0.0.2', '127.255.255.255')
        >>> r[-2:]
        IpRange('127.255.255.254', '127.255.255.255')
        >>> r[0:2]
        IpRange('127.0.0.1', '127.0.0.2')
        >>> r[0:-1]
        IpRange('127.0.0.1', '127.255.255.254')
        >>> r[:-2]
        IpRange('127.0.0.1', '127.255.255.253')
        >>> r[::2]
        Traceback (most recent call last):
            ...
        ValueError: slice step not supported
        """
        if isinstance(index, slice):
            if index.step not in (None, 1):
                #TODO: return an IpRangeList
                raise ValueError('slice step not supported')
            start = index.start or 0
            if start < 0:
                start = max(0, start + self._len)
            if start >= self._len:
                raise IndexError('start index out of range')

            stop = index.stop or self._len
            if stop < 0:
                stop = max(start, stop + self._len)
            if stop > self._len:
                raise IndexError('stop index out of range')
            return IpRange(
                    long2ip(self.startIp + start),
                    long2ip(self.startIp + stop - 1))

        else:
            if index < 0:
                index = self._len + index
            if index < 0 or index >= self._len:
                raise IndexError('index out of range')
            return long2ip(self.startIp + index)
    #end __getitem__

    def __iter__ (self):
        """
        Return an iterator over ip addresses in the range.


        >>> iter = IpRange('127/31').__iter__()
        >>> next(iter)
        '127.0.0.0'
        >>> next(iter)
        '127.0.0.1'
        >>> next(iter)
        Traceback (most recent call last):
            ...
        StopIteration
        """
        i = self.startIp
        while i <= self.endIp:
            yield long2ip(i)
            i += 1
    #end __iter__
#end class IpRange

class IpRangeList (object):
    """
    List of IpRange objects.

    Converts a list of dotted quad ip address and/or CIDR addresses into a
    list of IpRange objects. This list can perform ``in`` and ``not in`` tests
    and iterate all of the addresses in the range.

    This can be used to convert django's conf.settings.INTERNAL_IPS list into
    a smart object which allows CIDR notation.


    >>> INTERNAL_IPS = IpRangeList('127.0.0.1','10/8',('192.168.0.1','192.168.255.255'))
    >>> '127.0.0.1' in INTERNAL_IPS
    True
    >>> '10.10.10.10' in INTERNAL_IPS
    True
    >>> '192.168.192.168' in INTERNAL_IPS
    True
    >>> '172.16.0.1' in INTERNAL_IPS
    False


    :param \*args: List of ip addresses in dotted quad format or CIDR
        notation and/or ``(start, end)`` tuples of ip addresses in dotted quad
        format.
    :type \*args: list of str and/or tuple
    """
    def __init__ (self, *args):
        self.ips = tuple(map(IpRange, args))
    #end __init__

    def __repr__ (self):
        """
        >>> repr(IpRangeList('127.0.0.1', '10/8', '192.168/16'))
        "IpRangeList(IpRange('127.0.0.1', '127.0.0.1'), IpRange('10.0.0.0', '10.255.255.255'), IpRange('192.168.0.0', '192.168.255.255'))"
        >>> repr(IpRangeList(IpRange('127.0.0.1', '127.0.0.1'), IpRange('10.0.0.0', '10.255.255.255'), IpRange('192.168.0.0', '192.168.255.255')))
        "IpRangeList(IpRange('127.0.0.1', '127.0.0.1'), IpRange('10.0.0.0', '10.255.255.255'), IpRange('192.168.0.0', '192.168.255.255'))"
        """
        return "IpRangeList%r" % (self.ips,)
    #end __repr__

    def __str__ (self):
        """
        >>> str(IpRangeList('127.0.0.1', '10/8', '192.168/16'))
        "(('127.0.0.1', '127.0.0.1'), ('10.0.0.0', '10.255.255.255'), ('192.168.0.0', '192.168.255.255'))"
        """
        return "(%s)" % ", ".join(str(i) for i in self.ips)
    #end __str__

    def __contains__ (self, item):
        """
        Implements membership test operators ``in`` and ``not in`` for the
        address ranges contained in the list.


        >>> r = IpRangeList('127.0.0.1', '10/8', '192.168/16')
        >>> '127.0.0.1' in r
        True
        >>> '10.0.0.1' in r
        True
        >>> 2130706433 in r
        True
        >>> 'invalid' in r
        Traceback (most recent call last):
            ...
        TypeError: expected dotted-quad ip address or 32-bit integer


        :param item: Dotted-quad ip address.
        :type item: str
        :returns: ``True`` if address is in list, ``False`` otherwise.
        """
        for r in self.ips:
            if item in r:
                return True
        return False
    #end __contains__

    def __iter__ (self):
        """
        Return an iterator over all ip addresses in the list.

        >>> iter = IpRangeList('127.0.0.1').__iter__()
        >>> next(iter)
        '127.0.0.1'
        >>> next(iter)
        Traceback (most recent call last):
            ...
        StopIteration
        >>> iter = IpRangeList('127.0.0.1', '10/31').__iter__()
        >>> next(iter)
        '127.0.0.1'
        >>> next(iter)
        '10.0.0.0'
        >>> next(iter)
        '10.0.0.1'
        >>> next(iter)
        Traceback (most recent call last):
            ...
        StopIteration
        """
        for r in self.ips:
            for ip in r:
                yield ip
    #end __iter__

    def __len__ (self):
        """
        Return the length of all ranges in the list.


        >>> len(IpRangeList('127.0.0.1'))
        1
        >>> len(IpRangeList('127.0.0.1', '10/31'))
        3
        >>> len(IpRangeList('1/24'))
        256
        >>> len(IpRangeList('192.168.0.0/22'))
        1024
        """
        return sum([len(r) for r in self.ips])
    #end __len__
#end class IpRangeList

def iptools_test ():
    import doctest
    doctest.testmod()
#end iptools_test

if __name__ == '__main__':
   iptools_test()
# vim: set sw=4 ts=4 sts=4 et :

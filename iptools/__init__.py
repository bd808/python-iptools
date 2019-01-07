# -*- coding: utf-8 -*-
#
# Copyright (c) 2008-2014, Bryan Davis and iptools contributors
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
    def next(iterable):
        return iterable.next()

try:
    import Sequence
except ImportError:
    # python <2.6 doesn't have abc classes to extend
    Sequence = object
# end compatibility "fixes'

from . import ipv4
from . import ipv6

__version__ = '0.7.0'

__all__ = (
    'IpRange',
    'IpRangeList',
)


def _address2long(address):
    """
    Convert an address string to a long.
    """
    parsed = ipv4.ip2long(address)
    if parsed is None:
        parsed = ipv6.ip2long(address)
    return parsed
# end _addess2long


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
    >>> # IPv4 mapped IPv6 addresses are valid in an IPv4 block
    >>> '::ffff:127.127.127.127' in r
    True
    >>> # but only if they are actually in the block :)
    >>> '::ffff:192.0.2.128' in r
    False
    >>> '::ffff:c000:0280' in r
    False
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
    >>> r = IpRange('::ffff:0000:0000', '::ffff:ffff:ffff')
    >>> '::ffff:192.0.2.128' in r
    True
    >>> '::ffff:c000:0280' in r
    True
    >>> 281473902969472 in r
    True
    >>> '192.168.2.128' in r
    False
    >>> 2130706433 in r
    False
    >>> r = IpRange('::ffff:ffff:0000/120')
    >>> for ip in r:
    ...     print(ip) # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    ::ffff:ffff:0 ... ::ffff:ffff:6d ... ::ffff:ffff:ff


    :param start: Ip address in dotted quad format, CIDR notation, subnet
        format or ``(start, end)`` tuple of ip addresses in dotted quad format.
    :type start: str or tuple
    :param end: Ip address in dotted quad format or ``None``.
    :type end: str
    """
    def __init__(self, start, end=None):
        if end is None:
            if isinstance(start, IpRange):
                # copy constructor
                start, end = start[0], start[-1]

            elif isinstance(start, tuple):
                # occurs when IpRangeList calls via map to pass start and end
                start, end = start

            elif ipv4.validate_cidr(start):
                # CIDR notation range
                start, end = ipv4.cidr2block(start)

            elif ipv6.validate_cidr(start):
                # CIDR notation range
                start, end = ipv6.cidr2block(start)

            elif ipv4.validate_subnet(start):
                # Netmask notation range
                start, end = ipv4.subnet2block(start)

            else:
                # degenerate range
                end = start

        start = _address2long(start)
        end = _address2long(end)
        self.startIp = min(start, end)
        self.endIp = max(start, end)
        self._len = self.endIp - self.startIp + 1

        self._ipver = ipv4
        if self.endIp > ipv4.MAX_IP:
            self._ipver = ipv6
    # end __init__

    def __repr__(self):
        """
        >>> repr(IpRange('127.0.0.1'))
        "IpRange('127.0.0.1', '127.0.0.1')"
        >>> repr(IpRange('10/8'))
        "IpRange('10.0.0.0', '10.255.255.255')"
        >>> repr(IpRange('127.0.0.255', '127.0.0.0'))
        "IpRange('127.0.0.0', '127.0.0.255')"
        """
        return "IpRange(%r, %r)" % (
            self._ipver.long2ip(self.startIp),
            self._ipver.long2ip(self.endIp))
    # end __repr__

    def __str__(self):
        """
        >>> str(IpRange('127.0.0.1'))
        "('127.0.0.1', '127.0.0.1')"
        >>> str(IpRange('10/8'))
        "('10.0.0.0', '10.255.255.255')"
        >>> str(IpRange('127.0.0.255', '127.0.0.0'))
        "('127.0.0.0', '127.0.0.255')"
        """
        return (
            self._ipver.long2ip(self.startIp),
            self._ipver.long2ip(self.endIp)).__repr__()
    # end __str__

    def __eq__(self, other):
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
    # end __eq__

    def __len__(self):
        """
        Return the length of the range.


        >>> len(IpRange('127.0.0.1'))
        1
        >>> len(IpRange('127/31'))
        2
        >>> len(IpRange('127/22'))
        1024
        >>> IpRange('fe80::/10').__len__() == 2**118
        True
        """
        return self._len
    # end __len__

    def __hash__(self):
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
    # end __hash__

    def _cast(self, item):
        if isinstance(item, basestring):
            item = _address2long(item)
        if type(item) not in (type(1), type(ipv4.MAX_IP), type(ipv6.MAX_IP)):
            raise TypeError(
                "expected ip address, 32-bit integer or 128-bit integer")

        if ipv4 == self._ipver and item > ipv4.MAX_IP:
            # casting an ipv6 in an ipv4 range
            # downcast to ipv4 iff address is in the IPv4 mapped block
            if item in _IPV6_MAPPED_IPV4:
                item = item & ipv4.MAX_IP
        # end if

        return item
    # end _cast

    def index(self, item):
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
        raise ValueError('%s is not in range' % self._ipver.long2ip(item))
    # end index

    def count(self, item):
        return int(item in self)
    # end count

    def __contains__(self, item):
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
        TypeError: expected ip address, 32-bit integer or 128-bit integer


        :param item: Dotted-quad ip address.
        :type item: str
        :returns: ``True`` if address is in range, ``False`` otherwise.
        """
        item = self._cast(item)
        return self.startIp <= item <= self.endIp
    # end __contains__

    def __getitem__(self, index):
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
                # TODO: return an IpRangeList
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
                self._ipver.long2ip(self.startIp + start),
                self._ipver.long2ip(self.startIp + stop - 1))

        else:
            if index < 0:
                index = self._len + index
            if index < 0 or index >= self._len:
                raise IndexError('index out of range')
            return self._ipver.long2ip(self.startIp + index)
    # end __getitem__

    def __iter__(self):
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
            yield self._ipver.long2ip(i)
            i += 1
    # end __iter__
# end class IpRange


_IPV6_MAPPED_IPV4 = IpRange(ipv6.IPV4_MAPPED)


class IpRangeList (object):
    r"""
    List of IpRange objects.

    Converts a list of ip address and/or CIDR addresses into a list of IpRange
    objects. This list can perform ``in`` and ``not in`` tests and iterate all
    of the addresses in the range.

    :param \*args: List of ip addresses or CIDR notation and/or
            ``(start, end)`` tuples of ip addresses.
    :type \*args: list of str and/or tuple
    """
    def __init__(self, *args):
        self.ips = tuple(map(IpRange, args))
    # end __init__

    def __repr__(self):
        """
        >>> repr(IpRangeList('127.0.0.1', '10/8', '192.168/16'))
        ... #doctest: +NORMALIZE_WHITESPACE
        "IpRangeList(IpRange('127.0.0.1', '127.0.0.1'),
        IpRange('10.0.0.0', '10.255.255.255'),
        IpRange('192.168.0.0', '192.168.255.255'))"
        >>> repr(
        ...     IpRangeList(IpRange('127.0.0.1', '127.0.0.1'),
        ...     IpRange('10.0.0.0', '10.255.255.255'),
        ...     IpRange('192.168.0.0', '192.168.255.255')))
        ... #doctest: +NORMALIZE_WHITESPACE
        "IpRangeList(IpRange('127.0.0.1', '127.0.0.1'),
        IpRange('10.0.0.0', '10.255.255.255'),
        IpRange('192.168.0.0', '192.168.255.255'))"
        """
        return "IpRangeList%r" % (self.ips,)
    # end __repr__

    def __str__(self):
        """
        >>> str(IpRangeList('127.0.0.1', '10/8', '192.168/16'))
        ... #doctest: +NORMALIZE_WHITESPACE
        "(('127.0.0.1', '127.0.0.1'),
        ('10.0.0.0', '10.255.255.255'),
        ('192.168.0.0', '192.168.255.255'))"
        """
        return "(%s)" % ", ".join(str(i) for i in self.ips)
    # end __str__

    def __contains__(self, item):
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
        TypeError: expected ip address, 32-bit integer or 128-bit integer


        :param item: Dotted-quad ip address.
        :type item: str
        :returns: ``True`` if address is in list, ``False`` otherwise.
        """
        if isinstance(item, basestring):
            item = _address2long(item)
        if type(item) not in (type(1), type(ipv4.MAX_IP), type(ipv6.MAX_IP)):
            raise TypeError(
                "expected ip address, 32-bit integer or 128-bit integer")
        for r in self.ips:
            if item in r:
                return True
        return False
    # end __contains__

    def __iter__(self):
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
    # end __iter__

    def __len__(self):
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
        >>> IpRangeList('fe80::/10').__len__() == 2**118
        True
        """
        return sum(r.__len__() for r in self.ips)
    # end __len__

    def __hash__(self):
        """
        Return correct hash for IpRangeList object

        >>> a = IpRange('127.0.0.0/8')
        >>> b = IpRange('127.0.0.0', '127.255.255.255')
        >>> IpRangeList(a, b).__hash__() == IpRangeList(a, b).__hash__()
        True
        >>> IpRangeList(a, b).__hash__() == IpRangeList(b, a).__hash__()
        True
        >>> c = IpRange('10.0.0.0/8')
        >>> IpRangeList(a, c).__hash__() == IpRangeList(c, a).__hash__()
        False
        """
        return hash(self.ips)
    # end __hash__

    def __eq__(self, other):
        """
        >>> a = IpRange('127.0.0.0/8')
        >>> b = IpRange('127.0.0.0', '127.255.255.255')
        >>> IpRangeList(a, b) == IpRangeList(a, b)
        True
        >>> IpRangeList(a, b) == IpRangeList(b, a)
        True
        >>> c = IpRange('10.0.0.0/8')
        >>> IpRangeList(a, c) == IpRangeList(c, a)
        False
        """
        return hash(self) == hash(other)
    # end __eq__
# end class IpRangeList

# vim: set sw=4 ts=4 sts=4 et :

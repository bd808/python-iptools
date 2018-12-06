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

import re
from . import ipv4

__all__ = (
    'cidr2block',
    'ip2long',
    'long2ip',
    'long2rfc1924',
    'rfc19242long',
    'validate_cidr',
    'validate_ip',
    'DOCUMENTATION_NETWORK',
    'IPV4_MAPPED',
    'IPV6_TO_IPV4_NETWORK',
    'LINK_LOCAL',
    'LOCALHOST',
    'LOOPBACK',
    'MAX_IP',
    'MIN_IP',
    'MULTICAST',
    'MULTICAST_GLOBAL',
    'MULTICAST_LOCAL',
    'MULTICAST_LOCAL_DHCP',
    'MULTICAST_LOCAL_NODES',
    'MULTICAST_LOCAL_ROUTERS',
    'MULTICAST_LOOPBACK',
    'MULTICAST_SITE',
    'MULTICAST_SITE',
    'MULTICAST_SITE_DHCP',
    'PRIVATE_NETWORK',
    'TEREDO_NETWORK',
    'UNSPECIFIED_ADDRESS',
)

#: Regex for validating an IPv6 in hex notation
_HEX_RE = re.compile(r'^([0-9a-fA-F]{0,4}:){2,7}[0-9a-fA-F]{0,4}$')

#: Regex for validating an IPv6 in dotted-quad notation
_DOTTED_QUAD_RE = re.compile(r'^([0-9a-f]{0,4}:){2,6}(\d{1,3}\.){0,3}\d{1,3}$')

#: Regex for validating a CIDR network
_CIDR_RE = re.compile(r'^([0-9a-f]{0,4}:){2,7}[0-9a-f]{0,4}/\d{1,3}$')

#: Mamimum IPv6 integer
MAX_IP = 0xffffffffffffffffffffffffffffffff
#: Minimum IPv6 integer
MIN_IP = 0x0

#: Absence of an address (only valid as source address)
#: (`RFC 4291 <https://tools.ietf.org/html/rfc4291>`_)
UNSPECIFIED_ADDRESS = "::/128"

#: Loopback addresses on the local host
#: (`RFC 4291 <https://tools.ietf.org/html/rfc4291>`_)
LOOPBACK = "::1/128"

#: Common `localhost` address
#: (`RFC 4291 <https://tools.ietf.org/html/rfc4291>`_)
LOCALHOST = LOOPBACK

#: IPv4 mapped to IPv6 (not globally routable)
#: (`RFC 4291 <https://tools.ietf.org/html/rfc4291>`_)
IPV4_MAPPED = "::ffff:0:0/96"

#: Documentation and example network
#: (`RFC 3849 <https://tools.ietf.org/html/rfc3849>`_)
DOCUMENTATION_NETWORK = "2001::db8::/32"

#: 6to4 Address block
#: (`RFC 3056 <https://tools.ietf.org/html/rfc3056>`_)
IPV6_TO_IPV4_NETWORK = "2002::/16"

#: Teredo addresses
#: (`RFC 4380 <https://tools.ietf.org/html/rfc4380>`_)
TEREDO_NETWORK = "2001::/32"

#: Private network
#: (`RFC 4193 <https://tools.ietf.org/html/rfc4193>`_)
PRIVATE_NETWORK = "fd00::/8"

#: Link-Local unicast networks (not globally routable)
#: (`RFC 4291 <https://tools.ietf.org/html/rfc4291>`_)
LINK_LOCAL = "fe80::/10"

#: Multicast reserved block
#: (`RFC 5771 <https://tools.ietf.org/html/rfc5771>`_)
MULTICAST = "ff00::/8"

#: Interface-Local multicast
MULTICAST_LOOPBACK = "ff01::/16"

#: Link-Local multicast
MULTICAST_LOCAL = "ff02::/16"

#: Site-Local multicast
MULTICAST_SITE = "ff05::/16"

#: Organization-Local multicast
MULTICAST_SITE = "ff08::/16"

#: Organization-Local multicast
MULTICAST_GLOBAL = "ff0e::/16"

#: All nodes on the local segment
MULTICAST_LOCAL_NODES = "ff02::1"

#: All routers on the local segment
MULTICAST_LOCAL_ROUTERS = "ff02::2"

#: All DHCP servers and relay agents on the local segment
MULTICAST_LOCAL_DHCP = "ff02::1:2"

#: All DHCP servers and relay agents on the local site
MULTICAST_SITE_DHCP = "ff05::1:3"

#: RFC 1924 alphabet
_RFC1924_ALPHABET = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    '!', '#', '$', '%', '&', '(', ')', '*', '+', '-', ';', '<', '=',
    '>', '?', '@', '^', '_', '`', '{', '|', '}', '~',
]
#: RFC 1924 reverse lookup
_RFC1924_REV = None
#: Regex for validating an IPv6 in hex notation
_RFC1924_RE = re.compile(r'^[0-9A-Za-z!#$%&()*+-;<=>?@^_`{|}~]{20}$')


def validate_ip(s):
    """Validate a hexidecimal IPv6 ip address.


    >>> validate_ip('::')
    True
    >>> validate_ip('::1')
    True
    >>> validate_ip('2001:db8:85a3::8a2e:370:7334')
    True
    >>> validate_ip('2001:db8:85a3:0:0:8a2e:370:7334')
    True
    >>> validate_ip('2001:0db8:85a3:0000:0000:8a2e:0370:7334')
    True
    >>> validate_ip('2001:db8::1:0:0:1')
    True
    >>> validate_ip('ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff')
    True
    >>> validate_ip('::ffff:192.0.2.128')
    True
    >>> validate_ip('::ff::ff')
    False
    >>> validate_ip('::fffff')
    False
    >>> validate_ip('::ffff:192.0.2.300')
    False
    >>> validate_ip(None) #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    TypeError: expected string or buffer
    >>> validate_ip('1080:0:0:0:8:800:200c:417a')
    True


    :param s: String to validate as a hexidecimal IPv6 ip address.
    :type s: str
    :returns: ``True`` if a valid hexidecimal IPv6 ip address,
              ``False`` otherwise.
    :raises: TypeError
    """
    if _HEX_RE.match(s):
        return len(s.split('::')) <= 2
    if _DOTTED_QUAD_RE.match(s):
        halves = s.split('::')
        if len(halves) > 2:
            return False
        hextets = s.split(':')
        quads = hextets[-1].split('.')
        for q in quads:
            if int(q) > 255:
                return False
        return True
    return False
# end validate_ip


def ip2long(ip):
    """Convert a hexidecimal IPv6 address to a network byte order 128-bit
    integer.


    >>> ip2long('::') == 0
    True
    >>> ip2long('::1') == 1
    True
    >>> expect = 0x20010db885a3000000008a2e03707334
    >>> ip2long('2001:db8:85a3::8a2e:370:7334') == expect
    True
    >>> ip2long('2001:db8:85a3:0:0:8a2e:370:7334') == expect
    True
    >>> ip2long('2001:0db8:85a3:0000:0000:8a2e:0370:7334') == expect
    True
    >>> expect = 0x20010db8000000000001000000000001
    >>> ip2long('2001:db8::1:0:0:1') == expect
    True
    >>> expect = 281473902969472
    >>> ip2long('::ffff:192.0.2.128') == expect
    True
    >>> expect = 0xffffffffffffffffffffffffffffffff
    >>> ip2long('ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff') == expect
    True
    >>> ip2long('ff::ff::ff') == None
    True
    >>> expect = 21932261930451111902915077091070067066
    >>> ip2long('1080:0:0:0:8:800:200C:417A') == expect
    True


    :param ip: Hexidecimal IPv6 address
    :type ip: str
    :returns: Network byte order 128-bit integer or ``None`` if ip is invalid.
    """
    if not validate_ip(ip):
        return None

    if '.' in ip:
        # convert IPv4 suffix to hex
        chunks = ip.split(':')
        v4_int = ipv4.ip2long(chunks.pop())
        if v4_int is None:
            return None
        chunks.append('%x' % ((v4_int >> 16) & 0xffff))
        chunks.append('%x' % (v4_int & 0xffff))
        ip = ':'.join(chunks)

    halves = ip.split('::')
    hextets = halves[0].split(':')
    if len(halves) == 2:
        h2 = halves[1].split(':')
        for z in range(8 - (len(hextets) + len(h2))):
            hextets.append('0')
        for h in h2:
            hextets.append(h)
    # end if

    lngip = 0
    for h in hextets:
        if '' == h:
            h = '0'
        lngip = (lngip << 16) | int(h, 16)
    return lngip
# end ip2long


def long2ip(l, rfc1924=False):
    """Convert a network byte order 128-bit integer to a canonical IPv6
    address.


    >>> long2ip(2130706433)
    '::7f00:1'
    >>> long2ip(42540766411282592856904266426630537217)
    '2001:db8::1:0:0:1'
    >>> long2ip(MIN_IP)
    '::'
    >>> long2ip(MAX_IP)
    'ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff'
    >>> long2ip(None) #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    TypeError: unsupported operand type(s) for >>: 'NoneType' and 'int'
    >>> long2ip(-1) #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    TypeError: expected int between 0 and <really big int> inclusive
    >>> long2ip(MAX_IP + 1) #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    TypeError: expected int between 0 and <really big int> inclusive
    >>> long2ip(ip2long('1080::8:800:200C:417A'), rfc1924=True)
    '4)+k&C#VzJ4br>0wv%Yp'
    >>> long2ip(ip2long('::'), rfc1924=True)
    '00000000000000000000'


    :param l: Network byte order 128-bit integer.
    :type l: int
    :param rfc1924: Encode in RFC 1924 notation (base 85)
    :type rfc1924: bool
    :returns: Canonical IPv6 address (eg. '::1').
    :raises: TypeError
    """
    if MAX_IP < l or l < MIN_IP:
        raise TypeError(
            "expected int between %d and %d inclusive" % (MIN_IP, MAX_IP))

    if rfc1924:
        return long2rfc1924(l)

    # format as one big hex value
    hex_str = '%032x' % l
    # split into double octet chunks without padding zeros
    hextets = ['%x' % int(hex_str[x:x + 4], 16) for x in range(0, 32, 4)]

    # find and remove left most longest run of zeros
    dc_start, dc_len = (-1, 0)
    run_start, run_len = (-1, 0)
    for idx, hextet in enumerate(hextets):
        if '0' == hextet:
            run_len += 1
            if -1 == run_start:
                run_start = idx
            if run_len > dc_len:
                dc_len, dc_start = (run_len, run_start)
        else:
            run_len, run_start = (0, -1)
    # end for
    if dc_len > 1:
        dc_end = dc_start + dc_len
        if dc_end == len(hextets):
            hextets += ['']
        hextets[dc_start:dc_end] = ['']
        if dc_start == 0:
            hextets = [''] + hextets
    # end if

    return ':'.join(hextets)
# end long2ip


def long2rfc1924(l):
    """Convert a network byte order 128-bit integer to an rfc1924 IPv6
    address.


    >>> long2rfc1924(ip2long('1080::8:800:200C:417A'))
    '4)+k&C#VzJ4br>0wv%Yp'
    >>> long2rfc1924(ip2long('::'))
    '00000000000000000000'
    >>> long2rfc1924(MAX_IP)
    '=r54lj&NUUO~Hi%c2ym0'


    :param l: Network byte order 128-bit integer.
    :type l: int
    :returns: RFC 1924 IPv6 address
    :raises: TypeError
    """
    if MAX_IP < l or l < MIN_IP:
        raise TypeError(
            "expected int between %d and %d inclusive" % (MIN_IP, MAX_IP))
    o = []
    r = l
    while r > 85:
        o.append(_RFC1924_ALPHABET[r % 85])
        r = r // 85
    o.append(_RFC1924_ALPHABET[r])
    return ''.join(reversed(o)).zfill(20)


def rfc19242long(s):
    """Convert an RFC 1924 IPv6 address to a network byte order 128-bit
    integer.


    >>> expect = 0
    >>> rfc19242long('00000000000000000000') == expect
    True
    >>> expect = 21932261930451111902915077091070067066
    >>> rfc19242long('4)+k&C#VzJ4br>0wv%Yp') == expect
    True
    >>> rfc19242long('pizza') == None
    True
    >>> rfc19242long('~~~~~~~~~~~~~~~~~~~~') == None
    True
    >>> rfc19242long('=r54lj&NUUO~Hi%c2ym0') == MAX_IP
    True


    :param ip: RFC 1924  IPv6 address
    :type ip: str
    :returns: Network byte order 128-bit integer or ``None`` if ip is invalid.
    """
    global _RFC1924_REV
    if not _RFC1924_RE.match(s):
        return None
    if _RFC1924_REV is None:
        _RFC1924_REV = {v: k for k, v in enumerate(_RFC1924_ALPHABET)}
    x = 0
    for c in s:
        x = x * 85 + _RFC1924_REV[c]
    if x > MAX_IP:
        return None
    return x


def validate_cidr(s):
    """Validate a CIDR notation ip address.

    The string is considered a valid CIDR address if it consists of a valid
    IPv6 address in hextet format followed by a forward slash (/) and a bit
    mask length (0-128).


    >>> validate_cidr('::/128')
    True
    >>> validate_cidr('::/0')
    True
    >>> validate_cidr('fc00::/7')
    True
    >>> validate_cidr('::ffff:0:0/96')
    True
    >>> validate_cidr('::')
    False
    >>> validate_cidr('::/129')
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
            if int(mask) > 128:
                return False
        else:
            return False
        return True
    return False
# end validate_cidr


def cidr2block(cidr):
    """Convert a CIDR notation ip address into a tuple containing the network
    block start and end addresses.


    >>> cidr2block('2001:db8::/48')
    ('2001:db8::', '2001:db8:0:ffff:ffff:ffff:ffff:ffff')
    >>> cidr2block('::/0')
    ('::', 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff')


    :param cidr: CIDR notation ip address (eg. '127.0.0.1/8').
    :type cidr: str
    :returns: Tuple of block (start, end) or ``None`` if invalid.
    :raises: TypeError
    """
    if not validate_cidr(cidr):
        return None

    ip, prefix = cidr.split('/')
    prefix = int(prefix)
    ip = ip2long(ip)

    # keep left most prefix bits of ip
    shift = 128 - prefix
    block_start = ip >> shift << shift

    # expand right most 128 - prefix bits to 1
    mask = (1 << shift) - 1
    block_end = block_start | mask
    return (long2ip(block_start), long2ip(block_end))
# end cidr2block

# vim: set sw=4 ts=4 sts=4 et :

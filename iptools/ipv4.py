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

# sniff for python2.x / python3k compatibility "fixes'
try:
    basestring = basestring
except NameError:
    # 'basestring' is undefined, must be python3k
    basestring = str

try:
    bin = bin
except NameError:
    # builtin bin function doesn't exist
    def bin(x):
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
    # end bin
# end compatibility "fixes'

__all__ = (
    'cidr2block',
    'hex2ip',
    'ip2hex',
    'ip2long',
    'ip2network',
    'long2ip',
    'netmask2prefix',
    'subnet2block',
    'validate_cidr',
    'validate_ip',
    'validate_netmask',
    'validate_subnet',
    'BENCHMARK_TESTS',
    'BROADCAST',
    'CURRENT_NETWORK',
    'DUAL_STACK_LITE',
    'IETF_PROTOCOL_RESERVED',
    'IPV6_TO_IPV4_RELAY',
    'LINK_LOCAL',
    'LOCALHOST',
    'LOOPBACK',
    'MAX_IP',
    'MIN_IP',
    'MULTICAST',
    'MULTICAST_INTERNETWORK',
    'MULTICAST_LOCAL',
    'PRIVATE_NETWORK_10',
    'PRIVATE_NETWORK_172_16',
    'PRIVATE_NETWORK_192_168',
    'RESERVED',
    'SHARED_ADDRESS_SPACE',
    'TEST_NET_1',
    'TEST_NET_2',
    'TEST_NET_3',
)

#: Regex for validating an IPv4 address
_DOTTED_QUAD_RE = re.compile(r'^(\d{1,3}\.){0,3}\d{1,3}$')

#: Regex for validating a CIDR network
_CIDR_RE = re.compile(r'^(\d{1,3}\.){0,3}\d{1,3}/\d{1,2}$')

#: Mamimum IPv4 integer
MAX_IP = 0xffffffff
#: Minimum IPv4 integer
MIN_IP = 0x0

#: Broadcast messages to the current network (only valid as source address)
#: (`RFC 5735 <https://tools.ietf.org/html/rfc5735>`_)
CURRENT_NETWORK = "0.0.0.0/8"

#: Private network
#: (`RFC 1918 <https://tools.ietf.org/html/rfc1918>`_)
PRIVATE_NETWORK_10 = "10.0.0.0/8"

#: Carrier-grade NAT private network
#: (`RFC 6598 <https://tools.ietf.org/html/rfc6598>`_)
SHARED_ADDRESS_SPACE = "100.64.0.0/10"

#: Loopback addresses on the local host
#: (`RFC 5735 <https://tools.ietf.org/html/rfc5735>`_)
LOOPBACK = "127.0.0.0/8"

#: Common `localhost` address
#: (`RFC 5735 <https://tools.ietf.org/html/rfc5735>`_)
LOCALHOST = "127.0.0.1"

#: Autoconfiguration when no IP address available
#: (`RFC 3972 <https://tools.ietf.org/html/rfc3972>`_)
LINK_LOCAL = "169.254.0.0/16"

#: Private network
#: (`RFC 1918 <https://tools.ietf.org/html/rfc1918>`_)
PRIVATE_NETWORK_172_16 = "172.16.0.0/12"

#: IETF protocol assignments reserved block
#: (`RFC 5735 <https://tools.ietf.org/html/rfc5735>`_)
IETF_PROTOCOL_RESERVED = "192.0.0.0/24"

#: Dual-Stack Lite link address
#: (`RFC 6333 <https://tools.ietf.org/html/rfc6333>`_)
DUAL_STACK_LITE = "192.0.0.0/29"

#: Documentation and example network
#: (`RFC 5737 <https://tools.ietf.org/html/rfc5737>`_)
TEST_NET_1 = "192.0.2.0/24"

#: 6to4 anycast relay
#: (`RFC 3068 <https://tools.ietf.org/html/rfc3068>`_)
IPV6_TO_IPV4_RELAY = "192.88.99.0/24"

#: Private network
#: (`RFC 1918 <https://tools.ietf.org/html/rfc1918>`_)
PRIVATE_NETWORK_192_168 = "192.168.0.0/16"

#: Inter-network communications testing
#: (`RFC 2544 <https://tools.ietf.org/html/rfc2544>`_)
BENCHMARK_TESTS = "198.18.0.0/15"

#: Documentation and example network
#: (`RFC 5737 <https://tools.ietf.org/html/rfc5737>`_)
TEST_NET_2 = "198.51.100.0/24"

#: Documentation and example network
#: (`RFC 5737 <https://tools.ietf.org/html/rfc5737>`_)
TEST_NET_3 = "203.0.113.0/24"

#: Multicast reserved block
#: (`RFC 5771 <https://tools.ietf.org/html/rfc5771>`_)
MULTICAST = "224.0.0.0/4"

#: Link local multicast
#: (`RFC 5771 <https://tools.ietf.org/html/rfc5771>`_)
MULTICAST_LOCAL = "224.0.0.0/24"

#: Forwardable multicast
#: (`RFC 5771 <https://tools.ietf.org/html/rfc5771>`_)
MULTICAST_INTERNETWORK = "224.0.1.0/24"

#: Former Class E address space. Reserved for future use
#: (`RFC 1700 <https://tools.ietf.org/html/rfc1700>`_)
RESERVED = "240.0.0.0/4"

#: Broadcast messages to the current network
#: (only valid as destination address)
#: (`RFC 919 <https://tools.ietf.org/html/rfc919>`_)
BROADCAST = "255.255.255.255"


def validate_ip(s):
    """Validate a dotted-quad ip address.

    The string is considered a valid dotted-quad address if it consists of
    one to four octets (0-255) seperated by periods (.).


    >>> validate_ip('127.0.0.1')
    True
    >>> validate_ip('127.0')
    True
    >>> validate_ip('127.0.0.256')
    False
    >>> validate_ip(LOCALHOST)
    True
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
# end validate_ip


def validate_cidr(s):
    """Validate a CIDR notation ip address.

    The string is considered a valid CIDR address if it consists of a valid
    IPv4 address in dotted-quad format followed by a forward slash (/) and
    a bit mask length (1-32).


    >>> validate_cidr('127.0.0.1/32')
    True
    >>> validate_cidr('127.0/8')
    True
    >>> validate_cidr('127.0.0.256/32')
    False
    >>> validate_cidr('127.0.0.0')
    False
    >>> validate_cidr(LOOPBACK)
    True
    >>> validate_cidr('127.0.0.1/33')
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
# end validate_cidr


def validate_netmask(s):
    """Validate that a dotted-quad ip address is a valid netmask.


    >>> validate_netmask('0.0.0.0')
    True
    >>> validate_netmask('128.0.0.0')
    True
    >>> validate_netmask('255.0.0.0')
    True
    >>> validate_netmask('255.255.255.255')
    True
    >>> validate_netmask(BROADCAST)
    True
    >>> validate_netmask('128.0.0.1')
    False
    >>> validate_netmask('1.255.255.0')
    False
    >>> validate_netmask('0.255.255.0')
    False


    :param s: String to validate as a dotted-quad notation netmask.
    :type s: str
    :returns: ``True`` if a valid netmask, ``False`` otherwise.
    :raises: TypeError
    """
    if validate_ip(s):
        # Convert to binary string, strip '0b' prefix, 0 pad to 32 bits
        mask = bin(ip2network(s))[2:].zfill(32)
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
# end validate_netmask


def validate_subnet(s):
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
# end validate_subnet


def ip2long(ip):
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
        quads = quads[:-1] + [0, ] * (4 - len(quads)) + host

    lngip = 0
    for q in quads:
        lngip = (lngip << 8) | int(q)
    return lngip
# end ip2long


def ip2network(ip):
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
# end ip2network


def long2ip(l):
    """Convert a network byte order 32-bit integer to a dotted quad ip
    address.


    >>> long2ip(2130706433)
    '127.0.0.1'
    >>> long2ip(MIN_IP)
    '0.0.0.0'
    >>> long2ip(MAX_IP)
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
    >>> long2ip(MAX_IP + 1) #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    TypeError: expected int between 0 and 4294967295 inclusive


    :param l: Network byte order 32-bit integer.
    :type l: int
    :returns: Dotted-quad ip address (eg. '127.0.0.1').
    :raises: TypeError
    """
    if MAX_IP < l or l < MIN_IP:
        raise TypeError(
            "expected int between %d and %d inclusive" % (MIN_IP, MAX_IP))
    return '%d.%d.%d.%d' % (
        l >> 24 & 255, l >> 16 & 255, l >> 8 & 255, l & 255)
# end long2ip


def ip2hex(addr):
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
# end ip2hex


def hex2ip(hex_str):
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
# end hex2ip


def cidr2block(cidr):
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
# end cidr2block


def netmask2prefix(mask):
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
# end netmask2prefix


def subnet2block(subnet):
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
# end subnet2block


def _block_from_ip_and_prefix(ip, prefix):
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
# end _block_from_ip_and_prefix

# vim: set sw=4 ts=4 sts=4 et :

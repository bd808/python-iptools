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

import re
_HEX_RE = re.compile(r'^([0-9a-f]{0,4}:){2,7}[0-9a-f]{0,4}$')

def validate_ip (s):
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
    >>> validate_ip('::ff::ff')
    False
    >>> validate_ip('::fffff')
    False
    >>> validate_ip(None) #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    TypeError: expected string or buffer


    :param s: String to validate as a hexidecimal IPv6 ip address.
    :type s: str
    :returns: ``True`` if a valid hexidecimal IPv6 ip address, ``False`` otherwise.
    :raises: TypeError
    """
    if _HEX_RE.match(s):
        return len(s.split('::')) <= 2
    return False
#end validate_ip

def ip2long (ip):
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
    >>> expect = 0xffffffffffffffffffffffffffffffff
    >>> ip2long('ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff') == expect
    True
    >>> ip2long('ff::ff::ff') == None
    True


    :param ip: Hexidecimal IPv6 address
    :type ip: str
    :returns: Network byte order 128-bit integer or ``None`` if ip is invalid.
    """
    if not validate_ip(ip):
        return None

    halves = ip.split('::')
    hextets = halves[0].split(':')
    if len(halves) == 2:
        h2 = halves[1].split(':')
        for z in xrange(8 - (len(hextets) + len(h2))):
            hextets.append('0')
        for h in h2:
            hextets.append(h)
    #end if

    lngip = 0
    for h in hextets:
        if '' == h:
            h = '0'
        lngip = (lngip << 16) | int(h, 16)
    return lngip
#end ip2long


def _test ():
    import doctest
    failure, nbtest = doctest.testmod()
    if failure:
        import sys
        sys.exit(1)
#end _test

if __name__ == '__main__':
    _test()

# vim: set sw=4 ts=4 sts=4 et :

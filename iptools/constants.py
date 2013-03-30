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
"""Common and special use IPv4 address blocks."""

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

#: Broadcast messages to the current network (only valid as destination address)
#: (`RFC 919 <https://tools.ietf.org/html/rfc919>`_)
BROADCAST = "255.255.255.255"

# vim: set sw=4 ts=4 sts=4 et :

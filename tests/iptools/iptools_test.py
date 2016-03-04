# -*- coding: utf-8 -*-

import unittest
import iptools


class IpRangeListTests(unittest.TestCase):

    def testMixedRange(self):
        INTERNAL_IPS = iptools.IpRangeList(
            '127.0.0.1',                # single ip
            '192.168/16',               # CIDR network block
            ('10.0.0.1', '10.0.0.19'),  # arbitrary inclusive range
            '::1',                      # single IPv6 address
            'fe80::/10',                # IPv6 CIDR block
            '::ffff:0:0/96',            # IPv4-mapped IPv6
        )

        self.assertTrue('127.0.0.1' in INTERNAL_IPS)

        self.assertTrue('192.168.0.1' in INTERNAL_IPS)
        self.assertTrue('192.168.255.254' in INTERNAL_IPS)

        self.assertTrue('10.0.0.1' in INTERNAL_IPS)
        self.assertTrue('10.0.0.19' in INTERNAL_IPS)

        self.assertTrue('::1' in INTERNAL_IPS)

        self.assertTrue('fe80::1' in INTERNAL_IPS)
        self.assertTrue('fe80::ffff' in INTERNAL_IPS)
        self.assertTrue(
            'fe80:ffff:ffff:ffff:ffff:ffff:ffff:ffff' in INTERNAL_IPS)

        self.assertTrue('::ffff:172.16.11.12' in INTERNAL_IPS)

        self.assertFalse('209.19.170.129' in INTERNAL_IPS)
    # end testMixedRange
# end class IpRangeListTests


class IpRangeTests(unittest.TestCase):

    def testIPv6Range(self):
        fixture = iptools.IpRange('::ffff:0:0/96')
        self.assertTrue('::ffff:172.16.11.12' in fixture)
        self.assertFalse('209.19.170.129' in fixture)
    # end testIPv6Range

    def testV4MappedAddressInIPv6Range(self):
        """
        Given that the user has configured an IPv4 range
        When the server recieves a connection from a host in that range
         And the network stack presents that address in v4 mapped format
        Then the address should be recognized as being in the IPv4 range.
        """
        fixture = iptools.IpRange('192.168.0.1/24')

        self.assertTrue('192.168.0.12' in fixture)
        self.assertFalse('192.168.1.12' in fixture)

        self.assertTrue('::ffff:192.168.0.12' in fixture)
        self.assertFalse('::ffff:192.168.1.12' in fixture)
    # end test6to4AddressInIPv6Range
# end class IpRangeTests

# vim:se sw=4 ts=4 sts=4 et:

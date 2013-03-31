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
#end class IpRangeListTests


class IpRangeTests(unittest.TestCase):

    def testIPv6Range(self):
        fixture = iptools.IpRange('::ffff:0:0/96')
        self.assertTrue('::ffff:172.16.11.12' in fixture)
        self.assertFalse('209.19.170.129' in fixture)
    #end testIPv6Range
#end class IpRangeTests

# vim:se sw=4 ts=4 sts=4 et:

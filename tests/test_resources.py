#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_txccb
----------------------------------

Tests for `txccb` module.
"""

import os
import treq
import txccb
from txccb import resources
from twisted.trial import unittest
from twisted.internet import defer, reactor
from twisted.internet.tcp import Client
from twisted.internet.task import deferLater

url = os.environ.get('KINDRID_CCB_URL')
username = os.environ.get('KINDRID_CCB_USER')
password = os.environ.get('KINDRID_CCB_PASS')
txccb.configure(url, username, password)


class TestTxccb(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        def _check_fds(_):
            # This appears to only be necessary for HTTPS tests.
            # For the normal HTTP tests then closeCachedConnections is
            # sufficient.
            fds = set(reactor.getReaders() + reactor.getReaders())
            if not [fd for fd in fds if isinstance(fd, Client)]:
                return

            return deferLater(reactor, 0, _check_fds, None)

        if treq._utils.get_global_pool():
            return treq._utils.get_global_pool().closeCachedConnections().addBoth(_check_fds)

    @defer.inlineCallbacks
    def test_individual_search(self):
        out = yield resources.Individual.search(phone="5551212")
        self.assertIsInstance(out, list)

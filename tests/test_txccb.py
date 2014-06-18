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
from twisted.trial import unittest
from twisted.internet import defer, reactor
from twisted.internet.tcp import Client
from twisted.internet.task import deferLater


class TestTxccb(unittest.TestCase):

    def setUp(self):
        url = os.environ.get('KINDRID_CCB_URL')
        username = os.environ.get('KINDRID_CCB_USER')
        password = os.environ.get('KINDRID_CCB_PASS')
        self.client = txccb.configure(url, username, password)

    def tearDown(self):
        self.client = None

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
    def test_transaction_detail_type_list(self):
        out = yield self.client.transaction_detail_type_list()
        self.assertIsInstance(out, list)

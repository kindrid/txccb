#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_txccb
----------------------------------

Tests for `txccb` module.
"""

import os
import glob
import mock
import treq
import txccb
from txccb import resources
from twisted.trial import unittest
from twisted.internet import defer, reactor
from twisted.internet.tcp import Client
from twisted.internet.task import deferLater
from twisted.web.client import ResponseDone
from twisted.python.failure import Failure

url = os.environ.get('KINDRID_CCB_URL')
username = os.environ.get('KINDRID_CCB_USER')
password = os.environ.get('KINDRID_CCB_PASS')
txccb.configure(url, username, password)

TEST_DATA = {}
data_path = os.path.join(os.path.dirname(__file__), 'data', '*.xml')
for f in glob.glob(data_path):
    with open(f) as fp:
        name = os.path.basename(f)[:-4]
        TEST_DATA[name] = fp.read()


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

    def _create_deferred(self, code=200, content=None):
        response = mock.Mock()
        response.code = code
        if not content:
            content = ''
        response.length = len(content)
        response.deliverBody = self._deliverBody(content)
        return defer.succeed(response)

    def _deliverBody(self, content):
        def deliverBody(bodyCollector):
            bodyCollector.dataReceived(content)
            bodyCollector.connectionLost(Failure(ResponseDone()))
        return deliverBody

    @defer.inlineCallbacks
    def test_individual_search(self):
        key = "individual_search"
        ret = self._create_deferred(content=TEST_DATA[key])
        with mock.patch('treq.client.HTTPClient.request', return_value=ret):
            out = yield resources.Individual.search(phone="5551212")
        self.assertIsInstance(out, list)
        self.assertEqual(len(out), 4)

    @defer.inlineCallbacks
    def test_transaction_detail_type_list(self):
        key = "transaction_detail_type_list"
        ret = self._create_deferred(content=TEST_DATA[key])
        with mock.patch('treq.client.HTTPClient.request', return_value=ret):
            out = yield resources.TransactionDetailType.get_list()
        self.assertIsInstance(out, list)
        self.assertEqual(len(out), 52)

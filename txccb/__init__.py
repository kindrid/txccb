#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Trenton Broughton'
__email__ = 'trenton@kindrid.com'
__version__ = '0.1.1'


from txccb import config, client
from txccb.resources import Gift, Individual, TransactionDetailType


def configure(url=None, username=None, password=None):
    c = config.Config(url, username, password)
    client.client.config = c
    return client.client

__all__ = [
    'configure', 'config', 'client', 'resources', 'Gift',
    'Individual', 'TransactionDetailType'
]

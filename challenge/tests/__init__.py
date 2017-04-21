"""
Tests
=====

"""

import unittest

import sys

from challenge.connection import RedisConnection
from configuration import config
from tests.read_file_test import ApplicationReadTest
from tests.closest_empty_test import ApplicationCloseEmptyTest
from tests.closest_full_test import ApplicationCloseFullTest
from tests.search_test import ApplicationSearchTest

try:
    s = config.Settings(environment='test')
    RedisConnection(s).get_redis()
except Exception as e:
    print('Could not connect to Redis. Check that Redis is up and your settings are updated.')
    sys.exit(-1)

def all_tests():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ApplicationReadTest))
    suite.addTest(unittest.makeSuite(ApplicationCloseEmptyTest))
    suite.addTest(unittest.makeSuite(ApplicationCloseFullTest))
    suite.addTest(unittest.makeSuite(ApplicationSearchTest))
    return suite
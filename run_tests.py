#!/usr/bin/env python3

import sys
import unittest

import tests.search_tests as search
import tests.chat_tests as tests


if __name__ == '__main__':
    suite = unittest.TestSuite((
        unittest.makeSuite(search.SearchJobsTest),
        unittest.makeSuite(search.SearchFreelancersTest),

        unittest.makeSuite(tests.ChatTest),
    ))
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())

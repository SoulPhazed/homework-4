#!/usr/bin/env python3

import sys
import unittest

import tests.search_tests as search


if __name__ == '__main__':
    suite = unittest.TestSuite((
        unittest.makeSuite(search.SearchFindJobByTagTest),
        unittest.makeSuite(search.SearchFindJobByTitleTest),
        unittest.makeSuite(search.SearchCrossToJobPageTest)
    ))
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())

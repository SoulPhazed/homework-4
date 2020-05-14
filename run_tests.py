#!/usr/bin/env python3

import sys
import unittest

import tests.search_tests as search
import tests.chat_tests as chat
import tests.user_menu_tests as user_menu


if __name__ == '__main__':
    suite = unittest.TestSuite((
        unittest.makeSuite(search.SearchJobsTest),
        unittest.makeSuite(search.SearchFreelancersTest),

        unittest.makeSuite(chat.ChatTest),

        unittest.makeSuite(user_menu.UserMenuTest)
    ))
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())

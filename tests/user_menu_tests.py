import os
import unittest

from selenium.webdriver import DesiredCapabilities, Remote
from steps.auth_steps import AuthSteps
from steps.user_menu_steps import UserMenuSteps
from steps.profile_for_search import ProfileStepsForSearch


class UserMenuTest(unittest.TestCase):
    AUTH_ATTEMPTS = 5

    URLS = {
        "contracts": "/my-contracts",
        "profile": "/freelancers/",
        "proposals": "/proposals",
        "settings": "/settings",
        "postings": "/my-job-postings"
    }

    def setUp(self):
        browser = os.environ.get('BROWSER', 'CHROME')

        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )

    def tearDown(self):
        self.driver.quit()

    def login_to_role(self, role):
        auth_steps = AuthSteps(self.driver)

        for i in range(self.AUTH_ATTEMPTS):
            if role == "freelancer":
                status = auth_steps.login_as_freelancer()
            elif role == "client":
                status = auth_steps.login_as_client()
            else:
                status = True
            if status is True:
                break

    def test_cross_to_contracts(self):
        user_menu = UserMenuSteps(self.driver)

        self.login_to_role(role="freelancer")
        user_menu.to_contracts()
        self.assertTrue(user_menu.check_url(self.URLS["contracts"]))

    def test_cross_to_settings(self):
        user_menu = UserMenuSteps(self.driver)

        self.login_to_role(role="freelancer")
        user_menu.to_settings()
        self.assertTrue(user_menu.check_url(self.URLS["settings"]))

    def test_logout(self):
        user_menu = UserMenuSteps(self.driver)

        self.login_to_role(role="freelancer")
        user_menu.logout()
        self.assertTrue(user_menu.check_unauth())

    def test_cross_to_profile(self):
        user_menu = UserMenuSteps(self.driver)

        self.login_to_role(role="freelancer")
        user_menu.to_profile()
        self.assertTrue(user_menu.check_url(self.URLS["profile"]))

    def test_profile_data(self):
        user_menu = UserMenuSteps(self.driver)
        profile_steps = ProfileStepsForSearch(self.driver)

        self.login_to_role(role="freelancer")

        fl_name = profile_steps.get_profile_name()

        user_menu.to_profile()
        fl_info = profile_steps.get_info()

        self.assertTrue(fl_name["first_name"] == fl_info["first_name"] and fl_name["last_name"] == fl_info["last_name"])

    def test_cross_to_proposals(self):
        user_menu = UserMenuSteps(self.driver)

        self.login_to_role(role="freelancer")
        user_menu.to_proposals()
        self.assertTrue(user_menu.check_url(self.URLS["proposals"]))

    def test_cross_to_postings(self):
        user_menu = UserMenuSteps(self.driver)

        self.login_to_role(role="client")
        user_menu.to_postings()
        self.assertTrue(user_menu.check_url(self.URLS["postings"]))

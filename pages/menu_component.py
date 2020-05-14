import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException

from tests.general import Component


class ProfileMenu(Component):
    LOGIN_BUTTON = '//header//a[@href="/login"]'
    DROPDOWN_TOGGLE = '//header//button[contains(@class, "dropdown__toggle") and .//img]'

    CONTRACTS = '//header//a[contains(@href, "contracts")]'
    JOBS = '//header//a[contains(@href, "postings")]'
    PROFILE = '//header//a[starts-with(@href, "/freelancers")]'
    PROPOSALS = '//header//a[contains(@href, "proposals")]'
    SETTINGS = '//header//a[contains(@href, "settings")]'
    LOGOUT = '//a[@id = "logout"]'

    def toggle(self):
        toggle_btn = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.DROPDOWN_TOGGLE))
        )
        toggle_btn.click()

    def go_to_contracts(self):
        link = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.CONTRACTS))
        )

        link.click()

    def go_to_postings(self):
        link = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.JOBS))
        )

        link.click()

    def go_to_proposals(self):
        link = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.PROPOSALS))
        )

        link.click()

    def go_to_profile(self):
        link = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.PROFILE))
        )

        link.click()

    def go_to_settings(self):
        link = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.SETTINGS))
        )

        link.click()

    def logout(self):
        link = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.LOGOUT))
        )

        link.click()

    def check_crossing(self, old_url):
        try:
            WebDriverWait(self.driver, 3).until(
                ec.url_changes(old_url)
            )
        except TimeoutException:
            return False
        return True

    def check_url(self, url_to_compare):
        try:
            WebDriverWait(self.driver, 5).until(
                ec.url_contains(url_to_compare)
            )
        except TimeoutException:
            return False
        return True

    def check_unauth(self):
        try:
            WebDriverWait(self.driver, 5).until(
                ec.visibility_of_element_located((By.XPATH, self.LOGIN_BUTTON))
            )
        except TimeoutException:
            return False
        return True

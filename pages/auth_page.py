from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException

from tests.general import Page, Component


class AuthPage(Page):
    PATH = '/login'

    @property
    def form(self):
        return AuthForm(self.driver)


class AuthForm(Component):
    LOGIN = '//input[@name="email"]'
    PASSWORD = '//input[@name="password"]'
    SUBMIT = '//form[@id="loginForm"]//button[@type="submit"]'

    LOGIN_ERROR = '//form[@id="loginForm"]//div[contains(@class, "response-text-error")]'

    def set_login(self, login):
        self.driver.find_element_by_xpath(self.LOGIN).send_keys(login)

    def set_password(self, pwd):
        self.driver.find_element_by_xpath(self.PASSWORD).send_keys(pwd)

    def submit(self):
        element = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, self.SUBMIT))
        )
        element.click()

    def wait_for_login(self):
        try:
            WebDriverWait(self.driver, 5).until(
                ec.url_contains("dashboard")
            )
        except TimeoutException:
            return False
        return True

    def is_failed_to_fetch(self):
        try:
            login_error = WebDriverWait(self.driver, 1).until(
                ec.visibility_of_element_located((By.XPATH, self.LOGIN_ERROR))
            )
            if login_error.text == "Failed to fetch":
                return True
            return False
        except TimeoutException:
            return False

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

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

    def set_login(self, login):
        self.driver.find_element_by_xpath(self.LOGIN).send_keys(login)

    def set_password(self, pwd):
        self.driver.find_element_by_xpath(self.PASSWORD).send_keys(pwd)

    def submit(self):
        element = WebDriverWait(self.driver, 20).until(
            ec.element_to_be_clickable((By.XPATH, self.SUBMIT))
        )
        element.click()

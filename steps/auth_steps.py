import os

from tests.general import Step
from pages.auth_page import AuthPage


class AuthSteps(Step):
    def login(self, username, password):
        auth_page = AuthPage(self.driver)
        auth_page.open()

        form = auth_page.form
        form.set_login(username)
        form.set_password(password)
        form.submit()

    def login_as_freelancer(self, avoid_fetch_error=True):
        auth_page = AuthPage(self.driver)
        auth_page.open()
        form = auth_page.form
        form.set_login(os.getenv('F_EMAIL') if os.getenv('F_EMAIL') else 'anjou.naruko@list.ru')
        form.set_password(os.getenv('F_PASS') if os.getenv('F_PASS') else '111111')
        form.submit()

        if avoid_fetch_error:
            self.submit_if_failed_to_fetch()
        return form.wait_for_login()

    def login_as_client(self, avoid_fetch_error=True):
        auth_page = AuthPage(self.driver)
        auth_page.open()
        form = auth_page.form
        form.set_login(os.getenv('C_EMAIL') if os.getenv('C_EMAIL') else 'vlasov@mail.ru')
        form.set_password(os.getenv('C_PASS') if os.getenv('C_PASS') else '111111')
        form.submit()

        if avoid_fetch_error:
            self.submit_if_failed_to_fetch()
        return form.wait_for_login()

    def submit_if_failed_to_fetch(self):
        auth_page = AuthPage(self.driver)
        if auth_page.form.is_failed_to_fetch():
            auth_page.form.submit()

from tests.general import Step
from pages.user_menu_page import UserMenuPage


class UserMenuSteps(Step):
    def logout(self):
        page = UserMenuPage(self.driver)
        page.user_menu.toggle()
        page.user_menu.logout()

    def to_contracts(self):
        page = UserMenuPage(self.driver)
        page.user_menu.toggle()
        page.user_menu.go_to_contracts()

    def to_settings(self):
        page = UserMenuPage(self.driver)
        page.user_menu.toggle()
        page.user_menu.go_to_settings()

    def to_profile(self):
        page = UserMenuPage(self.driver)
        page.user_menu.toggle()
        page.user_menu.go_to_profile()

    def to_proposals(self):
        page = UserMenuPage(self.driver)
        page.user_menu.toggle()
        page.user_menu.go_to_proposals()

    def to_postings(self):
        page = UserMenuPage(self.driver)
        page.user_menu.toggle()
        page.user_menu.go_to_postings()

    def check_url(self, url_to_compare):
        page = UserMenuPage(self.driver)
        return page.user_menu.check_url(url_to_compare)

    def check_unauth(self):
        page = UserMenuPage(self.driver)
        return page.user_menu.check_unauth()
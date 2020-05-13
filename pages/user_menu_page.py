from tests.general import Page
from pages.menu_component import ProfileMenu


class UserMenuPage(Page):
    PATH = '/dashboard'

    @property
    def user_menu(self):
        return ProfileMenu(self.driver)

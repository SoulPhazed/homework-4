from tests.general import Step
from pages.profile_for_search import FreelancerPage
from pages.search_page import SearchPage


class ProfileStepsForSearch(Step):
    def get_info(self):
        freelancer_page = FreelancerPage(self.driver)
        search_page = SearchPage(self.driver)
        search_page.open()
        search_page.user_menu.toggle()
        search_page.user_menu.go_to_profile()

        return freelancer_page.info.get_info()

    def get_profile_id(self):
        page = FreelancerPage(self.driver)
        return page.info.get_id()

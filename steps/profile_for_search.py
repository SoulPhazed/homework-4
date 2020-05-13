import time
from tests.general import Step
from pages.profile_for_search import FreelancerPage, FreelancerSettingsPage
from pages.search_page import SearchPage


class ProfileStepsForSearch(Step):
    def get_info(self):
        freelancer_page = FreelancerPage(self.driver)
        search_page = SearchPage(self.driver)
        search_page.open()

        search_page.user_menu.toggle()
        search_page.user_menu.go_to_profile()
        # status = search_page.user_menu.check_crossing(search_url)
        # if status is True:
        #     break

        return freelancer_page.info.get_info()

    def get_profile_id(self):
        page = FreelancerPage(self.driver)
        return page.info.get_id()

    def open_settings_form(self):
        page = FreelancerSettingsPage(self.driver)
        page.open()

    def set_description(self, description):
        page = FreelancerSettingsPage(self.driver)
        page.form.set_description(description)

    def set_skills(self, skills):
        page = FreelancerSettingsPage(self.driver)
        page.form.set_skills(skills)

    def submit_settings(self):
        page = FreelancerSettingsPage(self.driver)
        page.form.submit()

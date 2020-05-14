from tests.general import Step
from pages.profile_for_search import FreelancerPage, FreelancerSettingsPage, AccountSettingsPage
from pages.search_page import SearchPage


class ProfileStepsForSearch(Step):
    def get_info(self):
        freelancer_page = FreelancerPage(self.driver)
        return freelancer_page.info.get_info()

    def get_profile_id(self):
        page = FreelancerPage(self.driver)
        return page.info.get_id()

    def get_profile_name(self):
        page = AccountSettingsPage(self.driver)
        page.open()
        return page.form.get_name()

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
